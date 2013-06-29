CARHUB_MOBILE=../CarHubMobile/CarHubMobile
LIB_VERSION=1.15.0-rc

# Generate the Java client library
endpointscfg.py get_client_lib java -o . -f rest api.CarHubApi

# Unzip the generated zip
mv CarHubApi.zip /tmp/CarHubApi.zip
unzip CarHubApi.zip

# Remove existing Jars from the libs folder of Android app
rm $CARHUB_MOBILE/CarHub/libs/google-*.jar
rm $CARHUB_MOBILE/CarHub/libs/gson-*.jar
rm $CARHUB_MOBILE/CarHub/libs/jsr-*.jar

# Copy new jars to the Android app
cp carhub/libs/gson-*.jar $CARHUB_MOBILE/CarHub/libs/
cp carhub/libs/jsr-*.jar $CARHUB_MOBILE/CarHub/libs/
cp carhub/libs/google-api-client-*.jar $CARHUB_MOBILE/CarHub/libs/
cp carhub/libs/google-api-client-$LIB_VERSION.jar $CARHUB_MOBILE/CarHub/libs/
cp carhub/libs/google-api-client-android-$LIB_VERSION.jar $CARHUB_MOBILE/CarHub/libs/
cp carhub/libs/google-http-client-$LIB_VERSION.jar $CARHUB_MOBILE/CarHub/libs/
cp carhub/libs/google-http-client-android-$LIB_VERSION.jar $CARHUB_MOBILE/CarHub/libs/
cp carhub/libs/google-http-client-gson-$LIB_VERSION.jar $CARHUB_MOBILE/CarHub/libs/
cp carhub/libs/google-oauth-client-$LIB_VERSION.jar $CARHUB_MOBILE/CarHub/libs/

# Get the java files out of the generated Jar
mv car-hub-carhub-*-java-$LIB_VERSION-sources.jar car-hub-carhub.zip
unzip car-hub-carhub.zip

cp -R car-hub-carhub-v1/com/google/* $CARHUB_MOBILE/CarHub/src/main/java/com/google/
