import boto3
from pprint import pprint
import inquirer

client = boto3.client("ec2")


def get_instance_id():
    response = client.describe_instances()["Reservations"]
    instance_ids = []

    for reservation in response:
        for instance in reservation["Instances"]:
            instance_ids.append(instance["InstanceId"])

    questions = [
        inquirer.List(
            "instance",
            message="Please select an instance",
            choices=instance_ids,
        ),
    ]

    answers = inquirer.prompt(questions)

    return answers["instance"]


def start_stop_instance(instance_id):
    response = client.describe_instances(InstanceIds=[instance_id])

    questions = [
        inquirer.List(
            "state",
            message="Please select a desired state of an instance",
            choices=["start", "stop", "terminate"],
        ),
    ]

    state_result = inquirer.prompt(questions)["state"]

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_state = instance["State"]["Name"]

    if state_result == "start":
        if instance_state in ["running", "pending"]:
            print(f"The instance is already in a {instance_state} state")
        else:
            client.start_instances(InstanceIds=[instance_id])
    elif state_result == "stop":
        if instance_state in ["stopping", "stopped"]:
            print(f"Instance is already in a {instance_state} state")
        else:
            client.stop_instances(InstanceIds=[instance_id])

    elif state_result == "terminate":
        if instance_state in ["terminated"]:
            print("Instance is already terminated")
        else:
            client.terminate_instances(InstanceIds=[instance_id])

    return "Response 200"


instance_id = get_instance_id()
print(start_stop_instance(instance_id))

def describe_instance(instance_id):
    response = client.describe_instances(InstanceIds=[instance_id])
    lst_outputs = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            outputs = {}
            outputs["imageId"] = instance["ImageId"]
            outputs["instanceId"] = instance["InstanceId"]
            outputs["type"] = instance["InstanceType"]
            outputs["keyName"] = instance["KeyName"]

            outputs["Networks"] = []
            network_outputs = {}
            network_outputs["publicIp"] = network["Association"]["PublicIP"]
            network_outputs["privateIp"]


           
            lst_outputs.append(outputs)

    return lst_outputs

