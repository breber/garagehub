GARAGEHUB_MOBILE=$(pwd)/../garagehub-android/GarageHubMobile
GARAGEHUB_IOS=$(pwd)/../garagehub-ios
LIB_VERSION=1.20.0

# Generate the Java client library
endpointscfg.py get_client_lib java -o . api.GarageHubApi

# Unzip the generated zip
mv garagehub-v1.zip /tmp/garagehubapi.zip
pushd /tmp/
yes | unzip garagehubapi.zip
pushd garagehub

# Remove existing Jars from the libs folder of Android app
rm $GARAGEHUB_MOBILE/GarageHub/libs/car_hub_appspot_*
rm $GARAGEHUB_MOBILE/GarageHub/libs/google-*
rm $GARAGEHUB_MOBILE/GarageHub/libs/gson-*
rm $GARAGEHUB_MOBILE/GarageHub/libs/jsr*

# Copy new jars to the Android app
cp *.jar $GARAGEHUB_MOBILE/GarageHub/libs/
cp libs/gson-*.jar $GARAGEHUB_MOBILE/GarageHub/libs/
cp libs/jsr*.jar $GARAGEHUB_MOBILE/GarageHub/libs/
cp libs/google-api-client-$LIB_VERSION.jar $GARAGEHUB_MOBILE/GarageHub/libs/
cp libs/google-api-client-android-$LIB_VERSION.jar $GARAGEHUB_MOBILE/GarageHub/libs/
cp libs/google-http-client-$LIB_VERSION.jar $GARAGEHUB_MOBILE/GarageHub/libs/
cp libs/google-http-client-android-$LIB_VERSION.jar $GARAGEHUB_MOBILE/GarageHub/libs/
cp libs/google-http-client-gson-$LIB_VERSION.jar $GARAGEHUB_MOBILE/GarageHub/libs/
cp libs/google-oauth-client-$LIB_VERSION.jar $GARAGEHUB_MOBILE/GarageHub/libs/

popd # /tmp/garagehub
popd # /tmp/

# Clean up after ourselves
rm /tmp/garagehubapi.zip
rm -rf /tmp/garagehub

# Generate for iOS
if [ -d $GARAGEHUB_IOS ]; then
    endpointscfg.py gen_discovery_doc -o . -f rpc api.GarageHubApi

    svn checkout \
        http://google-api-objectivec-client.googlecode.com/svn/trunk/ \
        google-api-objectivec-client-read-only

    pushd google-api-objectivec-client-read-only/Source/Tools/ServiceGenerator/
    xcodebuild -project ServiceGenerator.xcodeproj
    popd
    ./google-api-objectivec-client-read-only/Source/Tools/ServiceGenerator/build/Release/ServiceGenerator \
        garagehub-v1.discovery --outputDir $GARAGEHUB_IOS/GarageHubApi/

    rm -rf google-api-objectivec-client-read-only
fi
