import os
import io
import boto3
import json
import csv
import logging

runtime= boto3.client('runtime.sagemaker')
codepipeline = boto3.client('codepipeline')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Uncomment if you prefer to use environment variables
#ENDPOINT_NAME = os.environ['ENDPOINT_NAME']

# Not-defaulter data:
payload1 = '184.0, 2900.0, 0.98, 0.39, 5.0, 0.0, 0.51, 0.5, 4.21, 1.78, 0.02, 23.0, 0.12, 71.0, 40.85, 0.65, 1.02, 0.0, 0.00825206301575393, 4.0, 0.04, 0.96, 3999.0, 1.0, 33.0, 2971.0, 0.0, 0.58, 7.142857142857142, 1.0, 3.0, 6.7857142857142865, 5.0, 180.0, 19.0, 6.333333333333332, 0.03443657929978955, 0.04231625835189309, 0.030349013657056136, 127.0, 0.7055555555555556, 5.0, 0.04273504273504273, 6.143344709897611, 0.07, 1.89, 145.4, 0.77, 2599.0, 1038.0, 184.0, 12.0, 0.49, 20.0, 4.235171696149844, 110.0, 443.0, 99.0, 5422.0, 4.95, 407.0, 0.9366039039557782, 0.2816303946883069, 3.928571428571429, 0.3865732202139432, 132.0, 7.147376746638543, 2096.0, 0.6099225378089266, 3.083333333333333, 3307.0, 0.9187358916478556, 7.12, 4.54, 17.06, 4781.02, 438.94, 0.0, 1.45, 0.0, 22482.46, 1.0, 0.89, 0.0, 263691.34, 277.56, 0.92, 0.0, 339.35, 3.9586415365578294e-05, 3.4, 1.22, 0.0, 0.0, 1015.04, 0.0, 0.0, 379.52, 0.0, 0.0, 0.32, 0.0, 7.12, 1077023.92, 0.77, 0.0, 3.31, 0.0, 1225.2, 0.0, 0.02, 436.29, 0.0, 0.0, 95907.23, 74.76, 0.59, 41.322943430657, nan, 0.0, nan, 0.72, nan, nan, 0.82, 0.0, 0.0, nan, 60.1107199324761, 50.785041042695, nan, 0.0, 1.42, nan, 48.1914191364083, 0.0, 0.0, 32.95, 0.0, 0.0, 25.9, 0.0, 0.89, 0.0, nan, 24.37, nan, 0.0, nan, nan, nan, 0.0, nan, 0.57, nan, 0.0, nan, nan, 0.0, 34.5, nan, nan, nan, nan, nan, 0.52, 0.0, nan, 0.65, 0.0, nan, 0.0, 34.03, nan, 0.0, 0.0, 0.0, 49.9810437910087, 0.0, 1.05, 0.0, 1.0, 0.0, 100.0, 0.0, 5622.0, 0.0, 1.0, 1.0, 3.0, 1.35, 18.46, 0.0, 10.0, 0.0, 35.0, 50.0, 5422.0, 1.0, 10.0, 0.0, 1.2351362605839098, 35.3166, 9.0, 1.0377370041887801, 4.94, 83.0, 20.0, 4.65, 0.0, 0.0, 1527.0, 0.0, 0.0, 0.0, 37.0, 12.0, 4.44, 0.0, 136.0, 6.45, 18.15, 0.52, 0.35, 1.005, 0.86319050077439, 234.0, 16.72, 0.5118, 12.99, 12.68, 1.1144399999999999, 0.18, 16.6, 7.02, 21.89, 17.81, 0.6659999999999999, 0.73, 0.602, 3.63, 0.018069179143000002, 0.58, 4.6, 0.83, 153.33333333333334, 13.0, 0.02, 6.76, 0.0, 3.0, 196.0, 130000.0, 127.0, 0.03, 0.52, 30000.0, 0.0, 0.7, 0.03, 0.03, 0.0, 0.14545454545454545, 5789.0, 0.0, 0.2545454545454545, 0.0, 0.0, 0.1, 3.0, 0.6521, 0.8571, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 10000.0, 1.0, 1.0, 10000.0, 0.84, 0.0, 1.0, 0.0, 1.0, 1.5384, 3909.0, 33.33, 1.0, 0.0, 8.33, 0.0, 0.0, 5.56, 0.0, 0.0, 7.0, 0.0, 0.0, 1.1538, 0.0, 2.0, 10000.0, 1.5, 4.88, 0.0, 1.0, 0.14, 0.0, 0.0, 0.0, 1.2857, 0.0, 10000.0, 0.0, 2092.0, 141.0, 0.9225806451612903, 4995.0, 126.0, 0.413532481554795778'
# Defaulter data:
payload2 = '60.11, 110.0, 0.99, 0.09, 5.0, 0.77, 0.44, 0.5, 0.36, 2.29, 0.01, 48.0, 0.02, 1.0, 110.0, 0.64, 1.01, 0.71, 0.00495662949194547, 4.0, 0.02, 0.98, 807.0, 1.0, 4.0, 111.0, 1.33, 0.44, 0.0, 5.0, 11.0, 0.5128205128205128, 0.0, 39.0, 2.0, 0.18181818181818185, 0.0924170616113744, 0.0196078431372549, 0.07471264367816091, 39.0, 1.0, 0.0, 0.0, 0.8478260869565217, 0.96, 0.38, 31.43, 0.05, 62.46, 3.21252782376189, 60.11, 2.0, 0.7, 37.0, 1.297491039426523, 47.0, 213.0, 38.0, 753.0, 1.027027027027027, 181.0, 0.7926315789473685, 0.5046480743691899, 1.0734463276836157, 0.5498007968127491, 147.0, 0.668086239020495, 414.0, 0.694555112881806, 1.2312925170068028, 523.0, 0.8497652582159625, 10.02, 0.46, 10.43, 1172.27, 189.4, 0.0, 2.3, 0.0, 2196.57, 1.0, 0.0, 0.04, 211355.43, 84.48, 1.91, 0.0, 59.3, 0.0, 1.03, 0.7, 0.01, 0.02, 298.17, 0.689604842322592, 0.0, 227.86, 0.0, 52.07, 1.94, 0.02, 0.9, 395913.79, 0.31, 0.0, 1.28, 12.71, 83.74, 765.42, 0.1, 579.95, 0.01, 1.0, 8604.43, 130.06, 0.54, 70.1718644837339, 0.0, 0.0, 0.0, 0.56, 24.0, 9.0, 0.66, 0.0, 0.0, 19.0, 127.230466482265, 85.90011414995679, 55.0, 0.16, 1.07, 0.0, 71.6590049396513, 0.26, 0.0, 42.08, 0.0, 0.0, 37.45, 0.0, 1.08, 0.0, 10.0, 37.96, 90.0, 0.0, 19.0, 0.0, 55.0, 0.5, 28.0, 0.37, 0.0, 0.31, 40.0, 90.0, 0.16, 40.45, 38.0, 27.0, 173.0, 0.0, 178.0, 0.41, 0.24, 0.0, 0.49, 0.0, 0.0, 0.51, 46.57, 28.0, 0.32, 0.0, 0.0, 90.8904313776849, 0.52, 0.93, 1.0, 7.0, 0.0, 36.9236331328595, 0.0, 825.0, 0.0, 1.0, 1.0, 0.0, 1.53846153846154, 26.23, 0.0, 2.4935483870967703, 0.0, 6.125, 27.0, 753.0, 7.0, 83.0, 0.0, 1.5609320122090802, 21.6833, 310.0, 0.46524609707560494, 143.92, 13.0, 0.0, 0.91, 0.24, 21.0, 380.0, 1.65, 1.77, 80.0, 5.0, 41.0, 0.45, 0.45, 36.0, 0.89, 57.4, 0.41, 0.57, 0.1192, 0.94113029827315, 232.33333333333331, 23.98, 0.0784, 10.5, 11.08, 0.8849926199200001, 0.78, 28.5, 6.97, 27.37, 27.2, 0.0491, 0.39, 0.1769, 2.87, 0.022370486656200003, 0.4, 0.73, 0.57, 24.33333333333333, 28.0, 0.15, 0.71, 12.0, 18.0, 12.0, 2.33, 9.0, 0.13, 0.74, 100000.0, 0.0, 1.77, 0.13, 0.22, 0.0, 0.3193277310924369, 950.0, 0.0, 0.2689075630252101, 0.0, 0.9, 0.22, 10.0, 0.56, 0.6956, 10000.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.5384, 689.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.54, 0.0, 10000.0, 0.0, 4.0, 1.54, 1.0, 0.8571, 0.0, 1.0, 0.0, 1.4, 1.54, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.2, 0.0, 0.0, 1.0, 360.0, 24.0, 0.8343309106455751, 288.0, 48.0, 0.83793738489871088'

def defaulter_test(payload, endpoint):
    response = runtime.invoke_endpoint(EndpointName=endpoint,
                                       ContentType='text/csv',
                                       Body=payload)
    logger.debug(response)
    result = round(float(json.loads(response['Body'].read().decode())))
    logger.info(result)
    return result

def lambda_handler(event, context):

    job_id = event['CodePipeline.job']['id']
    ENDPOINT_NAME = event["CodePipeline.job"]['data']['actionConfiguration']['configuration']['UserParameters']
    
    try:

        logger.debug(json.dumps(event))
        
        logger.info('Running not defaulter test...')
        result = defaulter_test(payload1, ENDPOINT_NAME)
        if (result == 0):
            result1 = 'PASSED'
        else:
            result1 = 'FAILED'
        logger.info('Running defaulter test...')
        result = defaulter_test(payload2, ENDPOINT_NAME)
        if (result == 1):
            result2 = 'PASSED'
        else:
            result2 = 'FAILED'
        results = ('Not defaulter test: ' + result1 + ' - Defaulter test: ' + result2)
        logger.info(results)
 
        user_parameters = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']
        logger.debug(f'User parameters: {user_parameters}')
        response = codepipeline.put_job_success_result(jobId=job_id)
        logger.info(response)

    except Exception as error:
        logger.exception(error)
        response = codepipeline.put_job_failure_result(
            jobId=job_id,
            failureDetails={
                'type': 'JobFailed',
                'message': f'{error.__class__.__name__}: {str(error)}'
            }
        )
        logger.info(response)

    return response
