import os
import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

TABLE_NAME = os.environ.get('ORDERS_TABLE_NAME', 'EcommerceOrders')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')

table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        order_id = event.get('orderId')
        customer_id = event.get('customerId')
        total_amount = event.get('amount')
        
        # 1. Guardar transacción en DynamoDB
        table.put_item(
            Item={
                'orderId': order_id,
                'customerId': customer_id,
                'amount': str(total_amount),
                'status': 'COMPLETED',
                'createdAt': datetime.utcnow().isoformat()
            }
        )
        
        # 2. Publicar evento exitoso en SNS
        if SNS_TOPIC_ARN:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=f"Order Processed: {order_id}",
                Message=json.dumps({
                    "orderId": order_id,
                    "status": "SUCCESS",
                    "timestamp": datetime.utcnow().isoformat()
                })
            )
            
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Order processed and saved successfully',
                'orderId': order_id
            })
        }
        
    except Exception as e:
        print(f"Error persisting order: {str(e)}")
        raise e
