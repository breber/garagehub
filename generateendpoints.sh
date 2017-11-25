GARAGEHUB_MOBILE=$(pwd)/../garagehub-android/GarageHubMobile
LIB_VERSION=1.22.0

# Generate the Java client library
endpointscfg.py get_client_lib java -bs gradle -o . api.GarageHubApi

# Unzip the generated zip
mv garagehub-v1.zip /tmp/garagehubapi.zip
pushd /tmp/
yes | unzip garagehubapi.zip
pushd garagehub

# Remove existing classes from the com.appspot namespace of Android app
rm -rf $GARAGEHUB_MOBILE/GarageHub/src/main/java/com/appspot

# Copy new generated classes to the Android app
cp -r src/main/java/com/appspot $GARAGEHUB_MOBILE/GarageHub/src/main/java/com/appspot

popd # /tmp/garagehub
popd # /tmp/

# Clean up after ourselves
rm /tmp/garagehubapi.zip
rm -rf /tmp/garagehub
