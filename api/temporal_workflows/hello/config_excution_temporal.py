from pydantic import BaseModel


class ConfigTemporalWorflowyActivity(BaseModel):
    activity_name: str
    workflow_name: str
    task_queue: str


config_temporal_hello = ConfigTemporalWorflowyActivity(
    activity_name="your_activity", workflow_name="YourWorkflow", task_queue="hello-task-queue"
)


config_temporal_hello_eventarc = ConfigTemporalWorflowyActivity(
    activity_name="your_activity", workflow_name="YourWorkflowEventArc", task_queue="hello-task-queue-eventarc"
)
