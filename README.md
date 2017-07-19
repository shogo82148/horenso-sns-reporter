# horenso-sns-reporter
Amazon SNS reporter for [Songmu/horenso](https://github.com/Songmu/horenso)

``` bash
#!/bin/sh

# Amazon SNS topic to publish
export HORENSO_TOPIC_ARN=arn:aws:sns:ap-northeast-1:xxxxxxx:xxxxxx

# Comment out if you need success notification
export HORENSO_MUTE_ON_NORMAL=1

# Add access key if necessary
export AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxx
export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxx
export AWS_SESSION_TOKEN=xxxxxxxxxxxxxxxxxxx
export AWS_DEFAULT_REGION=ap-northeast-1

exec horenso -r "sh -c '/PATH/TO/REPORTER/reporter.py 2>&1 | logger -t reporter'" -- "$@"
```

## SEE ALSO

- [Songmu/horenso](https://github.com/Songmu/horenso)
- [horensoというcronやコマンドラッパー用のツールを書いた](http://www.songmu.jp/riji/entry/2016-01-05-horenso.html)
