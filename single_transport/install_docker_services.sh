# Run this script only once, when you first clone the gateway software. 
# Does:
#   1. Copies the .yml files into the right name
#   2. You have to manually change the gateway id afterwards in the service "transport service, gateway id"
#
#
#


cp sample_yaml_ACM0.yml docker-compose.yml
cp sample_yaml_ACM1.yml docker-compose_ACM1.yml

# now input the new gateway id

echo "Hi, write the gateway id for this device:"
read gw_id

line=$(grep "WM_GW_ID" sample_yaml_ACM0.yml -n | cut -d : -f 1)
sed -i $line's/.*/      WM_GW_ID: '$gw_id'/' docker-compose.yml

