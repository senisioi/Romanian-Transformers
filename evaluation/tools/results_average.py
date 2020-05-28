import os
import json
import argparse


def print_task_metrics(task_name, dict_metrics, counter, sub_unit=False):
    print("\n{}".format(task_name))
    print("|{:^9s}     |{:^11s}|{:^11s}|{:^11s}|".format("Metric", "Precision", "Recall", "F1 Score"))
    print("+--------------+-----------+-----------+-----------+")

    for metric in dict_metrics:
        print("| {:13s}|{:^11.2f}|{:^11.2f}|{:^11.2f}|".format(
            metric,
            dict_metrics[metric]["precision"] / counter * (100 if sub_unit else 1) if counter > 0 else 0,
            dict_metrics[metric]["recall"] / counter * (100 if sub_unit else 1) if counter > 0 else 0,
            dict_metrics[metric]["f1"] / counter * (100 if sub_unit else 1) if counter > 0 else 0,
        ))


def main():
    for lang_model_name in os.listdir(args.results_path):
        dict_metrics_ronec = {
            "Entity Type": {"precision": 0, "recall": 0, "f1": 0},
            "Partial": {"precision": 0, "recall": 0, "f1": 0},
            "Strict": {"precision": 0, "recall": 0, "f1": 0},
            "Exact": {"precision": 0, "recall": 0, "f1": 0}
        }
        dict_metrics_ronec_frozen = {
            "Entity Type": {"precision": 0, "recall": 0, "f1": 0},
            "Partial": {"precision": 0, "recall": 0, "f1": 0},
            "Strict": {"precision": 0, "recall": 0, "f1": 0},
            "Exact": {"precision": 0, "recall": 0, "f1": 0}
        }
        dict_metrics_rrt = {
            "UPOS": {"precision": 0, "recall": 0, "f1": 0},
            "XPOS": {"precision": 0, "recall": 0, "f1": 0}
        }
        dict_metrics_rrt_frozen = {
            "UPOS": {"precision": 0, "recall": 0, "f1": 0},
            "XPOS": {"precision": 0, "recall": 0, "f1": 0}
        }
        dict_metrics_rrt_udify = {
            "UPOS": {"precision": 0, "recall": 0, "f1": 0},
            "UFeats": {"precision": 0, "recall": 0, "f1": 0},
            "Lemmas": {"precision": 0, "recall": 0, "f1": 0},
            "LAS": {"precision": 0, "recall": 0, "f1": 0}
        }

        counter_rrt_frozen = 0
        counter_rrt = 0
        counter_rrt_udify = 0
        counter_ronec_frozen = 0
        counter_ronec = 0

        for filename in os.listdir(os.path.join(args.results_path, lang_model_name)):
            if "rrt_frozen" in filename:
                with open(os.path.join(args.results_path, lang_model_name, filename)) as file:
                    dict_metrics = json.load(file)

                for metric in dict_metrics_rrt_frozen:
                    dict_metrics_rrt_frozen[metric]["precision"] += dict_metrics[metric]["precision"]
                    dict_metrics_rrt_frozen[metric]["recall"] += dict_metrics[metric]["recall"]
                    dict_metrics_rrt_frozen[metric]["f1"] += dict_metrics[metric]["f1"]

                counter_rrt_frozen += 1

            elif "rrt_udify" in filename:
                with open(os.path.join(args.results_path, lang_model_name, filename)) as file:
                    dict_metrics = json.load(file)

                for metric in dict_metrics_rrt_udify:
                    dict_metrics_rrt_udify[metric]["precision"] += dict_metrics[metric]["precision"]
                    dict_metrics_rrt_udify[metric]["recall"] += dict_metrics[metric]["recall"]
                    dict_metrics_rrt_udify[metric]["f1"] += dict_metrics[metric]["f1"]

                counter_rrt_udify += 1

            elif "rrt" in filename:
                with open(os.path.join(args.results_path, lang_model_name, filename)) as file:
                    dict_metrics = json.load(file)

                for metric in dict_metrics_rrt:
                    dict_metrics_rrt[metric]["precision"] += dict_metrics[metric]["precision"]
                    dict_metrics_rrt[metric]["recall"] += dict_metrics[metric]["recall"]
                    dict_metrics_rrt[metric]["f1"] += dict_metrics[metric]["f1"]

                counter_rrt += 1

            elif "ronec_frozen" in filename:
                with open(os.path.join(args.results_path, lang_model_name, filename)) as file:
                    dict_metrics = json.load(file)

                for metric in dict_metrics_ronec_frozen:
                    dict_metrics_ronec_frozen[metric]["precision"] += dict_metrics[metric]["precision"]
                    dict_metrics_ronec_frozen[metric]["recall"] += dict_metrics[metric]["recall"]
                    dict_metrics_ronec_frozen[metric]["f1"] += dict_metrics[metric]["f1"]

                counter_ronec_frozen += 1

            elif "ronec" in filename:
                with open(os.path.join(args.results_path, lang_model_name, filename)) as file:
                    dict_metrics = json.load(file)

                for metric in dict_metrics_ronec:
                    dict_metrics_ronec[metric]["precision"] += dict_metrics[metric]["precision"]
                    dict_metrics_ronec[metric]["recall"] += dict_metrics[metric]["recall"]
                    dict_metrics_ronec[metric]["f1"] += dict_metrics[metric]["f1"]

                counter_ronec += 1

        print("Language model: {}".format(lang_model_name))

        print_task_metrics("RRT Frozen", dict_metrics_rrt_frozen, counter_rrt_frozen)
        print_task_metrics("RRT Non-Frozen", dict_metrics_rrt, counter_rrt)
        print_task_metrics("RRT UDify", dict_metrics_rrt_udify, counter_rrt_udify, sub_unit=True)
        print_task_metrics("RONEC Frozen", dict_metrics_ronec_frozen, counter_ronec_frozen)
        print_task_metrics("RONEC Non-Frozen", dict_metrics_ronec, counter_ronec)

        print("\n" + "-" * 52 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("results_path")

    args = parser.parse_args()

    main()