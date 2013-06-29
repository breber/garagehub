CARHUB_MOBILE=$(pwd)/../CarHubMobile/CarHubMobile
LIB_VERSION=1.15.0-rc

# Generate the Java client library
endpointscfg.py get_client_lib java -o . -f rest api.CarHubApi

# Unzip the generated zip
mv CarHubApi.zip /tmp/CarHubApi.zip
pushd /tmp/
yes | unzip CarHubApi.zip
pushd carhub

# Remove existing Jars from the libs folder of Android app
rm $CARHUB_MOBILE/CarHub/libs/google-*
rm $CARHUB_MOBILE/CarHub/libs/gson-*
rm $CARHUB_MOBILE/CarHub/libs/jsr*

# Copy new jars to the Android app
cp libs/gson-*.jar $CARHUB_MOBILE/CarHub/libs/
cp libs/jsr*.jar $CARHUB_MOBILE/CarHub/libs/
cp libs/google-api-client-$LIB_VERSION.jar $CARHUB_MOBILE/CarHub/libs/
cp libs/google-api-client-android-$LIB_VERSION.jar $CARHUB_MOBILE/CarHub/libs/
cp libs/google-http-client-$LIB_VERSION.jar $CARHUB_MOBILE/CarHub/libs/
cp libs/google-http-client-android-$LIB_VERSION.jar $CARHUB_MOBILE/CarHub/libs/
cp libs/google-http-client-gson-$LIB_VERSION.jar $CARHUB_MOBILE/CarHub/libs/
cp libs/google-oauth-client-$LIB_VERSION.jar $CARHUB_MOBILE/CarHub/libs/

# Get the java files out of the generated Jar
mv car-hub-carhub*.jar car-hub-carhub.zip
unzip car-hub-carhub.zip

cp -R com/google/* $CARHUB_MOBILE/CarHub/src/main/java/com/google/

popd # carhub
popd # /tmp/

# Clean up after ourselves
rm /tmp/CarHubApi.zip
rm -rf /tmp/carhub
