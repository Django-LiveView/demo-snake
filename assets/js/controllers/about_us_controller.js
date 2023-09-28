import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang } from "../mixins/miscellaneous.js";

export default class extends Controller {

    static targets = [];

    randomNumberText(event) {
	sendData(
	    {
		action: "home->random_number",
		data: {}
	    }
	);
    }
}
