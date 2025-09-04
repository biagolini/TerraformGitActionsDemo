import sys
import os
import boto3

def generate_ai_summary(plan_file_path, output_file_path, aws_region):
    """Generate AI summary of Terraform plan using AWS Bedrock"""
    
    # Read the Terraform plan
    with open(plan_file_path, 'r') as f:
        plan_content = f.read()
    
    # Configure Bedrock client
    client = boto3.client('bedrock-runtime', region_name=aws_region)
    
    # Prepare the prompt
    prompt = f"""Please analyze this Terraform plan and provide a concise summary of the infrastructure changes. Focus on:

1. Resources being created, modified, or destroyed
2. Key configuration changes
3. Potential impact on the infrastructure
4. Any security or cost implications

Keep the summary clear and non-technical for approval reviewers. Use only standard ASCII characters, avoid emojis.

Terraform Plan:
{plan_content}"""
    
    try:
        # Call Amazon Nova Lite
        response = client.converse(
            modelId='amazon.nova-lite-v1:0',
            messages=[{
                "role": "user",
                "content": [{"text": prompt}]
            }],
            inferenceConfig={"temperature": 0.3, "maxTokens": 500}
        )
        
        # Extract and clean the summary
        summary = response['output']['message']['content'][0]['text']
        # Remove any potential Unicode issues
        clean_summary = summary.encode('ascii', 'ignore').decode('ascii')
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(clean_summary)
        
        print("AI Summary generated successfully")
        return True
        
    except Exception as e:
        print(f"Error generating AI summary: {e}")
        # Create fallback summary
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("AI summary generation failed. Please review the full Terraform plan for details.")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python generate_ai_summary.py <plan_file> <output_file> <aws_region>")
        sys.exit(1)
    
    plan_file = sys.argv[1]
    output_file = sys.argv[2]
    aws_region = sys.argv[3]
    
    generate_ai_summary(plan_file, output_file, aws_region)