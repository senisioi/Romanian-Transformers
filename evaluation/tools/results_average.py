import os
import json
import argparse


def print_task_metrics(task_name, dict_metrics, counter, sub_unit=False):
    if counter == 0:
        return

    print("\n{}".format(task_name))
    print("|{:^9s}     |{:^11s}|{:^11s}|{:^11s}|".format("Metric", "Precision", "Recall", "F1 Score"))
    print("+--------------+-----------+-----------+-----------+")

    for metric in dict_metrics:
        print("| {:13s}|{:^11.2f}|{:^11.2f}|{:^11.2f}|".format(
            metric,
            dict_metrics[metric]["precision"] / counter * (100 if sub_unit else 1),
            dict_metrics[metric]["recall"] / counter * (100 if sub_unit else 1),
            dict_metrics[metric]["f1"] / counter * (100 if sub_unit else 1),
        ))


def update_metrics(filename, dict_metrics):
    with open(os.path.join(args.results_path, filename)) as file:
        dict_new_metrics = json.load(file)

    for metric in dict_metrics:
        dict_metrics[metric]["precision"] += dict_new_metrics[metric]["precision"]
        dict_metrics[metric]["recall"] += dict_new_metrics[metric]["recall"]
        dict_metrics[metric]["f1"] += dict_new_metrics[metric]["f1"]


def init_metrics_dictionaries():
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

    return dict_metrics_rrt_frozen, dict_metrics_rrt, \
           dict_metrics_rrt_udify, \
           dict_metrics_ronec_frozen, dict_metrics_ronec


def main():
    dict_metrics_rrt_frozen, dict_metrics_rrt, \
    dict_metrics_rrt_udify, \
    dict_metrics_ronec_frozen, dict_metrics_ronec = init_metrics_dictionaries()

    counter_rrt_frozen = counter_rrt = counter_rrt_udify = counter_ronec_frozen = counter_ronec = 0

    for filename in os.listdir(os.path.join(args.results_path)):
        if "rrt_frozen" in filename:
            update_metrics(filename, dict_metrics_rrt_frozen)
            counter_rrt_frozen += 1
        elif "rrt_udify" in filename:
            update_metrics(filename, dict_metrics_rrt_udify)
            counter_rrt_udify += 1
        elif "rrt" in filename:
            update_metrics(filename, dict_metrics_rrt)
            counter_rrt += 1
        elif "ronec_frozen" in filename:
            update_metrics(filename, dict_metrics_ronec_frozen)
            counter_ronec_frozen += 1
        elif "ronec" in filename:
            update_metrics(filename, dict_metrics_ronec)
            counter_ronec += 1

    print_task_metrics("RRT Frozen", dict_metrics_rrt_frozen, counter_rrt_frozen)
    print_task_metrics("RRT Non-Frozen", dict_metrics_rrt, counter_rrt)
    print_task_metrics("RRT UDify", dict_metrics_rrt_udify, counter_rrt_udify, sub_unit=True)
    print_task_metrics("RONEC Frozen", dict_metrics_ronec_frozen, counter_ronec_frozen)
    print_task_metrics("RONEC Non-Frozen", dict_metrics_ronec, counter_ronec)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("results_path")

    args = parser.parse_args()

    main()