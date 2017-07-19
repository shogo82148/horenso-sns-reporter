#!/bin/sh

export HORENSO_TOPIC_ARN=arn:aws:sns:ap-northeast-1:xxxxxxx:xxxxxx
export HORENSO_MUTE_ON_NORMAL=1
exec horenso -r "sh -c '/PATH/TO/REPORTER/reporter.py 2>&1 | logger -t reporter'" -- "$@"
