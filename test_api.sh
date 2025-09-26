#!/bin/bash

# Base URL
BASE_URL="http://localhost:8000"

echo "Testing API endpoints..."

# Test main endpoint
echo "\n1. Testing main endpoint:"
curl $BASE_URL

# Test admin endpoints
echo "\n\n2. Testing admin endpoints:"
echo "\nGetting all alerts:"
curl $BASE_URL/admin/alerts

# Test user endpoints
echo "\n\n3. Testing user endpoints:"
echo "\nGetting user alerts:"
curl $BASE_URL/user/alerts

# Test analytics
echo "\n\n4. Testing analytics:"
curl $BASE_URL/analytics/metrics

echo "\n\nTests complete!"