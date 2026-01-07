import { Controller } from "../vendors/stimulus.js";

export default class extends Controller {

    static targets = [];

    up(event) {
	event.preventDefault();
	// Create a fake button element with the liveview function data
	const button = document.createElement('button');
	button.setAttribute('data-liveview-function', 'key_up');
	// Trigger the page controller's run method
	const pageController = this.application.getControllerForElementAndIdentifier(document.body, 'page');
	if (pageController) {
	    const fakeEvent = new Event('click');
	    Object.defineProperty(fakeEvent, 'currentTarget', { value: button });
	    pageController.run(fakeEvent);
	}
    }

    right(event) {
	event.preventDefault();
	const button = document.createElement('button');
	button.setAttribute('data-liveview-function', 'key_right');
	const pageController = this.application.getControllerForElementAndIdentifier(document.body, 'page');
	if (pageController) {
	    const fakeEvent = new Event('click');
	    Object.defineProperty(fakeEvent, 'currentTarget', { value: button });
	    pageController.run(fakeEvent);
	}
    }

    down(event) {
	event.preventDefault();
	const button = document.createElement('button');
	button.setAttribute('data-liveview-function', 'key_down');
	const pageController = this.application.getControllerForElementAndIdentifier(document.body, 'page');
	if (pageController) {
	    const fakeEvent = new Event('click');
	    Object.defineProperty(fakeEvent, 'currentTarget', { value: button });
	    pageController.run(fakeEvent);
	}
    }

    left(event) {
	event.preventDefault();
	const button = document.createElement('button');
	button.setAttribute('data-liveview-function', 'key_left');
	const pageController = this.application.getControllerForElementAndIdentifier(document.body, 'page');
	if (pageController) {
	    const fakeEvent = new Event('click');
	    Object.defineProperty(fakeEvent, 'currentTarget', { value: button });
	    pageController.run(fakeEvent);
	}
    }
}
