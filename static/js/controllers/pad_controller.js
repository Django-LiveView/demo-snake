import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang } from "../mixins/miscellaneous.js";

export default class extends Controller {

    static targets = [];

    up(event) {
	sendData(
	    {
		action: "home->key_up",
		data: {}
	    }
	);
    }

    right(event) {
	sendData(
	    {
		action: "home->key_right",
		data: {}
	    }
	);
    }

    down(event) {
	sendData(
	    {
		action: "home->key_down",
		data: {}
	    }
	);
    }

    left(event) {
	sendData(
	    {
		action: "home->key_left",
		data: {}
	    }
	);
    }
}
