from examples import example_dict

available_examples = list(example_dict.keys())

print("Please choose one of the following scripts to run:")
for i, script_name in enumerate(available_examples):
    print("{0}) {1}".format(i + 1, script_name))

chosen_script = available_examples[int(input("Please type your chosen script number: ")) - 1]

print("Running {0}".format(chosen_script))

print("Please press 'Run Simulation' on the CoderZ website.")

example_dict[chosen_script]()
