import boto3
from typing import List, Dict

batch = boto3.client("batch")


def list_all_job_queues() -> List[Dict]:
    """Returns all job queues and their status/details."""
    resp = batch.describe_job_queues()
    return resp.get("jobQueues", [])


def list_running_jobs(job_queue: str, max_results: int = 100) -> List[Dict]:
    """Lists currently RUNNING jobs in the given job queue."""
    # You can also paginate if you expect more
    resp = batch.list_jobs(jobQueue=job_queue, jobStatus="RUNNING", maxResults=max_results)
    job_summary_list = resp.get("jobSummaryList", [])
    if not job_summary_list:
        return []
    # Optionally fetch more details per job
    job_ids = [j["jobId"] for j in job_summary_list]
    detailed = batch.describe_jobs(jobs=job_ids).get("jobs", [])
    return detailed


def submit_batch_job(
    job_name: str,
    job_queue: str,
    job_definition: str,
    parameters: Dict = None,
    container_overrides: Dict = None,
    depends_on: List[Dict] = None,
) -> Dict:
    """Submits a new job to AWS Batch."""
    kwargs = {
        "jobName": job_name,
        "jobQueue": job_queue,
        "jobDefinition": job_definition,
    }
    if parameters:
        kwargs["parameters"] = parameters
    if container_overrides:
        kwargs["containerOverrides"] = container_overrides
    if depends_on:
        kwargs["dependsOn"] = depends_on

    resp = batch.submit_job(**kwargs)
    return resp

if __name__ == "__main__":
    queues = list_all_job_queues()
    print("Job Queues:")
    for q in queues:
        print(f"  - Name: {q['jobQueueName']}, State: {q['state']}, Status: {q['status']}")
        running = list_running_jobs(q['jobQueueName'])
        print(f"\nRunning jobs in queue '{q['jobQueueName']}':")
        if running:
            for job in running:
                print(
                    f"  - {job['jobName']} (ID: {job['jobId']}), Status: {job['status']}, Started: {job.get('startedAt')}")

        print("="*100)