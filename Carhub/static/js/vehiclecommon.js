function getVehicleId() {
	return /\/vehicle\/([^\/]+)/.exec(window.location.pathname);
}