import json


def to_plantuml(json_data):
    plantuml = []
    plantuml.append('@startuml\n')
    plantuml.append('start\n')

    tasks = json_data['tasks']
    start_task = json_data['start_task']

    current_task = start_task
    for task in tasks:
        if task['type'] == 'normal':
            plantuml.append(f':{task["name"]};\n')
            if task["name"] == current_task:
                current_task = None

        if task['type'] == 'conditional':
            plantuml.append(f'if ({task["outgoing_tasks"][0]["condition"]}) then (yes)\n')
            plantuml.append(f'  :{task["outgoing_tasks"][0]["next_task"]};\n')
            plantuml.append(f'else (no)\n')
            plantuml.append(f'  :{task["outgoing_tasks"][1]["next_task"]};\n')
            plantuml.append('endif\n')
            if task["name"] == current_task:
                current_task = task["outgoing_tasks"][0]["next_task"]

    plantuml.append('stop\n')
    plantuml.append('@enduml\n')
    return ''.join(plantuml)


if __name__ == "__main__":
    with open("tests/test_data/data/tasks.json") as f:
        workflow = json.load(f)
    print(to_plantuml(workflow))
