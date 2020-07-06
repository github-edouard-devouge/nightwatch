import http from "../http-common";

class NightWatchDataService {
  getOutdatedImages() {
    return http.get("/outdated-images/");
  }

  getAllImages() {
    return http.get("/images/");
  }

  getImage(image_uuid) {
    return http.get(`/images/${image_uuid}`);
  }

  getStatus() {
    return http.get("/status");
  }

  watch() {
    return http.get("/watch");
  }

  start() {
    return http.get("/start");
  }

  stop() {
    return http.get("/stop");
  }
}


export default new NightWatchDataService();
