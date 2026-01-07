import { Application } from "./vendors/stimulus.js";
import homeController from "./controllers/home_controller.js";

/*
   INITIALIZATION
 */

// Stimulus
if (!window.Stimulus) {
    window.Stimulus = Application.start();
}

// Register custom controllers
Stimulus.register("home", homeController);
