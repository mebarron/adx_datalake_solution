import json
import boto3
import datetime

client = boto3.client('dataexchange')

def getDataSet(DataSetId):
    try:
        response = client.get_data_set(
        DataSetId=DataSetId
        )
        return response
    except Exception as e:
        raise(e)

def getRevision(DataSetId, RevisionId):
    try:
        response = client.get_revision(
        DataSetId=DataSetId,
        RevisionId=RevisionId
        )
        return response
    except Exception as e:
        raise(e)

def getAsset(AssetId, DataSetId, RevisionId):
    try:
        response = client.get_asset(
        AssetId='string',
        DataSetId='string',
        RevisionId='string'
        )
        return response
    except Exception as e:
        raise(e)

def listRevisionAssets(DataSetId, RevisionId):
    try:
        response = client.list_revision_assets(
        DataSetId=DataSetId,
        MaxResults=123,
        RevisionId=RevisionId
        )
        return response
    except Exception as e:
        raise(e)

def listDataSets():
    try:
        response = client.list_data_sets(
        MaxResults=123,
        Origin="ENTITLED"
        )
        return response
    except Exception as e:
        raise(e)

def listDataSetRevisions(DataSetId):
    try:
        response = client.list_data_set_revisions(
        DataSetId=DataSetId,
        MaxResults=123
        )
        return response
    except Exception as e:
        raise(e)

def createJob(JobConfiguration):
    try:
        response = client.create_job(
        Details=JobConfiguration,
        Type='EXPORT_ASSETS_TO_S3'
        )
        return response
    except Exception as e:
        raise(e)

def startJob(JobId):
    try:
        response = client.start_job(
        JobId=JobId
        )
        return response
    except Exception as e:
        raise(e)

def lambda_handler(event, context):
    DataSetId = event['Id']
    DataLakeRawBucket = event['DataLakeRawBucket']
    DataSetRevisions = listDataSetRevisions(DataSetId)
    DataSetRevisionsL = []
    for DataSetRevision in DataSetRevisions['Revisions']:
        DataSetRevisionsL.append(DataSetRevision['Id'])
    RevisionAssets = listRevisionAssets(DataSetId, DataSetRevisionsL[0])
    for i, DataSetRevisionId in enumerate(DataSetRevisionsL):
    RevisionAssetS3Key = RevisionAssets['Assets'][i]['Name']
    RevisionAssetId = RevisionAssets['Assets'][i]['Id']
    	JobConfig = {
        	'ExportAssetsToS3': {
            		'AssetDestinations': [
                	{
                    		'AssetId': RevisionAssetId,
                    		'Bucket': DataLakeRawBucket,
                    		'Key': RevisionAssetS3Key
                	},
            	],
            	'DataSetId': DataSetId,
            	'RevisionId': DataSetRevisionsL[i]
            	}
        }
	try:
		NewExportJob = createJob(JobConfig)
        	startJob(NewExportJob['Id'])
        	return "SUCCESS"
    	except Exception as e:
        	raise(e)
