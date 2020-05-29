#!/bin/bash

function nice_print {
	title=$1
	printf '\n%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' '#'

	printf "\n%*s" $((($(tput cols))/2 - 1 - (${#title})/2 + `if [ $(( $(tput cols) % 2 )) -eq 1 ]; then echo 1; else echo 0; fi`)) | tr ' ' '#'
	printf " $title "
	printf "%*s\n" $((($(tput cols))/2 - (${#title})/2 - 1)) | tr ' ' '#'

	printf '\n%*s\n\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' '#'
}

if [ -z "$1" ]; then
	echo "Please specify a model path/model name from HuggingFace's repositoy."
	exit 1
else
	model=$1
fi

device="cuda"

if [ -n "$2" ]; then
	device="$2"
fi

datetime=$(date +"%d-%m-%Y-%H-%M-%S")
model_basename=$(basename "$model")
model_dirs=("models/$model_basename/rrt_upos_frozen" "models/$model_basename/rrt_xpos_frozen" "models/$model_basename/rrt_upos" "models/$model_basename/rrt_xpos")
output_paths=("outputs/$model_basename/predict_rrt_upos_frozen.conllu" "outputs/$model_basename/predict_rrt_xpos_frozen.conllu" "outputs/$model_basename/predict_rrt_upos.conllu" "outputs/$model_basename/predict_rrt_xpos.conllu")
goals=("UPOS" "XPOS" "UPOS" "XPOS")
predict_cols=(3 4 3 4)
frozen=(true true false false)

nice_print "Training model on UD Romanian RRT..."

for i in {0..3}
do
  printf "Model: %s\n" "$1"
  printf "Save path: %s\n" "${model_dirs[i]}"
  printf "Frozen: %s\n" "${frozen[i]}"
  printf "Device: %s\n" "$device"
  printf "Training goal: %s\n\n" "${goals[i]}"


  [ ! -d "${model_dirs[i]}" ] && mkdir -p "${model_dirs[i]}"

  if [ "${frozen[i]}" == false ]; then
    fine_tune="--fine_tune"
    epochs=5
    learning_rate=2e-5
    batch_size=16
  else
    fine_tune=""
    epochs=100
    learning_rate=2e-4
    batch_size=128
  fi

  python3 tools/train.py dataset-rrt/train.conllu dataset-rrt/dev.conllu "${predict_cols[i]}" --save_path "${model_dirs[i]}" --lang_model_name "$model" --device $device $fine_tune --epochs $epochs --learning_rate $learning_rate --batch_size $batch_size --datetime "$datetime"

  printf '\n%*s\n\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' '#'
done

nice_print "Evaluating model on UD Romanian RRT..."

[ ! -d "outputs/$model_basename" ] && mkdir -p "outputs/$model_basename"
[ ! -d "results/$model_basename" ] && mkdir -p "results/$model_basename"

for i in {0..3}
do
	printf "Model: %s\n" "$1"
 	printf "Load path: %s\n" "${model_dirs[i]}"
	printf "Device: %s\n" "$device"
	printf "Evaluation goal: %s\n\n" "${goals[i]}"

	python3 tools/predict.py dataset-rrt/test.conllu "${model_dirs[i]}" "${predict_cols[i]}" --lang_model_name "$model" --output_path "${output_paths[i]}" --device "$device" --datetime "$datetime"

	printf '\n%*s\n\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' '#'
done

python3 tools/ud_unite.py "outputs/$model_basename" --frozen --datetime "$datetime"
python3 tools/ud_eval.py dataset-rrt/test.conllu "outputs/$model_basename/predict_rrt_frozen.conllu" --datetime "$datetime" --output_path "results/$model_basename/rrt_frozen.json"

python3 tools/ud_unite.py "outputs/$model_basename" --datetime "$datetime"
python3 tools/ud_eval.py dataset-rrt/test.conllu "outputs/$model_basename/predict_rrt.conllu" --datetime "$datetime" --output_path "results/$model_basename/rrt.json"

