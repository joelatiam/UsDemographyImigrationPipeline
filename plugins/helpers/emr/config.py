SPARK_STEPS = [
    {
        'Name': 'Clean immigration data Step',
        'ActionOnFailure': 'CANCEL_AND_WAIT',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                '--deploy-mode',
                'cluster',
                's3n://{{ params.S3_BUCKET }}/{{ params.S3_DIRECTORY }}/{{ params.S3_SCRIPT }}',
            ],
        },
    }
]

JOB_FLOW_OVERRIDES = {
    'Name': 'Clean Immigration',
    'ReleaseLabel': 'emr-5.33.0',
    'Instances': {
        'InstanceGroups': [
            {
                'Name': 'Master nodes',
                'Market': 'SPOT',
                'InstanceRole': 'MASTER',
                'InstanceType': 'm5.xlarge',
                'InstanceCount': 1,
            },
        ],
        'KeepJobFlowAliveWhenNoSteps': True,
        'TerminationProtected': False,
    },
    # 'Steps': SPARK_STEPS,
    'JobFlowRole': 'EMR_EC2_DefaultRole',
    'ServiceRole': 'EMR_DefaultRole',
}
