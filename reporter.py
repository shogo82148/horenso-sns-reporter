#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import print_function # Python 2/3 compatibility
import json
import sys
import string
import os
import argparse
import boto3

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help="name of alarm")
    args = parser.parse_args()

    report = json.load(sys.stdin)
    name = args.name or (report["hostname"] + ": " + report["command"])

    topic_arn = os.environ.get("HORENSO_TOPIC_ARN", None)
    if not topic_arn:
        print("HORENSO_TOPIC_ARN not found", file=sys.stderr)
        return

    mute_on_normal = os.environ.get("HORENSO_MUTE_ON_NORMAL", "0") != "0"
    if mute_on_normal and report["exitCode"] == 0:
        return

    region = "Unknown"
    template = string.Template(u"""Songmu/horenso report
$name
- Result:     $result
- StartAt:    $startAt
- EndAt:      $endAt
- UserTime:   $userTime
- SystemTime: $systemTime

Stdout:
$stdout

Stderr:
$stderr
""")
    text_message = template.substitute(name=name, **report)

    json_message = json.dumps({
        "AlarmName": name,
        "AlarmDescription": " ".join(report["commandArgs"]),
        "AWSAccountId": "0",
        "NewStateValue": "OK" if report["exitCode"] == 0 else "ALARM",
        "NewStateReason": report["result"] + "\n" + report["output"],
        "StateChangeTime": report["endAt"],
        "Region": region,
        "OldStateValue": "INSUFFICIENT_DATA",
        "Trigger": {
            "MetricName": " ".join(report["commandArgs"]),
            "Namespace": "Songmu/horenso",
            "StatisticType": "Statistic",
            "Statistic": "COUNT",
            "Unit": None,
            "Dimensions": [],
            "Period": 60,
            "EvaluationPeriods": 1,
            "ComparisonOperator": "GreaterThanThreshold",
            "Threshold": 0,
            "TreatMissingData": "- TreatMissingData: NonBreaching",
            "EvaluateLowSampleCountPercentile": "",
        },
    })

    message = json.dumps({
        "default": json_message,
        "email": text_message,
    })
    client = boto3.client('sns')
    print(client.publish(TopicArn=topic_arn, Message=message, MessageStructure="json"))

if __name__ == "__main__":
    main()
