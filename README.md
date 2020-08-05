## **Courier default use case - Amazon SageMaker workshop**

## **Overview**

Building and deploying automated machine learning (ML) and artificial intelligence (AI) projects in production often requires provisioning and integrating a different set of functions separately for orchestrating the pipelines.

In modern cloud architectures, typically following DevOps or CI/CD practices, this means connecting the data-science and operational worlds through a set of different services for covering each step of the workflows, consuming time and effort to set up these independently on each service.

In this sample project, you will explore how you can **reduce and optimize the efforts** in these tasks by:
* Leveraging on some Amazon SageMaker features
* Orchestrating the infrastructure from the same place with services like AWS Step Functions and its Data Science SDK for Amazon SageMaker
* Building CI/CD pipelines for your ML workloads

## **Instructions**

For running this lab you will need to:
* Create an Amazon S3 bucket
* Adjust the permissions for your AWS IAM role
* Create an Amazon SageMaker notebook instance
* Run the cells in the sample notebooks provided
You can do this with the following steps...

### **1. Create an Amazon S3 bucket**

- Open the Amazon S3 console for your account at https://console.aws.amazon.com/s3/.
- Choose "Create bucket", enter a bucket name that is unique e.g. try with your "name-lastname-mlops-workshop", for region choose "EU (Ireland)", and choose "Create".

### **2. Create an Amazon SageMaker notebook instance**

To create a Amazon SageMaker notebook instance:

- Open the Amazon SageMaker console for your account at https://console.aws.amazon.com/sagemaker/.
- Choose "Notebook instances", then choose Create notebook instance.
- On the "Create notebook instance" page, provide the following information:
  - For Notebook instance name, type a name for your notebook instance.
  - For Notebook instance type, choose "ml.t3.medium" unless told otherwise.
  - For IAM role, choose "Create a new role". In the pop-up window, for S3 buckets choose "Any S3 bucket" and hit "Create role". Amazon SageMaker creates an IAM role named "AmazonSageMaker-ExecutionRole-YYYYMMDDTHHmmSS". The AWS managed policy AmazonSageMakerFullAccess is attached to the role. The role provides permissions that allow the notebook instance to call Amazon SageMaker and Amazon S3. ***Note the name of this role, as you will need to attach additional permissions to it later.***
  - Back in the Create notebook interface, expand "Git repositories" and choose "Clone a public Git repository to this notebook instance only", then add the URL: https://github.com/rodzanto/courier-default
  - Finally choose "Create notebook instance".

In a few minutes, Amazon SageMaker launches an ML compute instance —in this case a notebook instance— and attaches an ML storage volume to it. The notebook instance has a preconfigured Jupyter notebook server and a set of Anaconda libraries.

When the status of the notebook instance is "InService" in the console, the notebook instance is ready to use.

You can continue with the next step in the meantime.

### 3. **Update your new AWS IAM role**

- Open the AWS IAM console for your account at https://console.aws.amazon.com/iam/.
- Choose "Roles", and search for the role you created in the previous step (it should be named "AmazonSageMaker-ExecutionRole-YYYYMMDDTHHmmSS"), and click on it.
- Choose "Attach policies", and search for "AWSLambdaFullAccess", select the checkbox next to it and choose "Attach policy". Repeat this step for attaching the policies "AmazonS3FullAccess", "IAMFullAccess", "AWSStepFunctionsFullAccess", "AWSCodePipeline-FullAccess". *Note in a real scenario we would split the tasks on different and more specific roles following a least-privilege policy*.
- Now choose "Trust relationships", and "Edit trust relationship". Replace the policy shown with the following for allowing the execution of the AWS Step Functions workflow in our notebook:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "states.amazonaws.com",
          "lambda.amazonaws.com",
          "sagemaker.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
- Then click "Update Trust Policy".

### 3. **Run the required notebooks for each lab**

- Go back to the Amazon SageMaker console, choose "Notebook instances", and open the notebook you created by choosing "Open Jupyter". Note the notebook instance should be in "In service" status for having this option.
- Click on the sample notebooks provided (in order), and go through the cells for each Lab as indicated by the workshop staff:
  - Lab #1: Data scientist sandbox [1.sandbox](./1.sandbox.ipynb)
  - Lab #2: Prepare the ML workflow [2.workflow](./2.workflow.ipynb)
  - Lab #3: Build the ML pipeline [3.pipeline](./3.pipeline.ipynb)
  follow the instructions provided in each one.

Note the following important tips:
  - Some cells require you to replace some placeholders with e.g. your bucket name, Account ID, or Role created before running. Make sure you read any comments before running those.
  - If it's the first time you work with Jupyter notebooks you can ask staff assistance. Remember you can run the cells one by one with Shift+Enter or the Run button in the top bar.
  - It is recommended to have the notebooks in "Trusted" status for keeping the cells outputs. If your notebook shows "Not trusted" in the top bar, you can click on it for choosing "Trust".

### **Some Links and Documentation:**

- [AWS Machine Learning Overview](https://aws.amazon.com/machine-learning/?nc1=h_ls)
- [AWS Machine Learning Blog](https://aws.amazon.com/blogs/machine-learning/?nc1=h_ls)
- [Amazon SageMaker documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
- [AWS Step Functions Data Science Python SDK documentation](https://aws-step-functions-data-science-sdk.readthedocs.io/en/latest/index.html)
- [AWS Step Functions Data Science Python SDK GitHub repository](https://github.com/aws/aws-step-functions-data-science-sdk-python)

