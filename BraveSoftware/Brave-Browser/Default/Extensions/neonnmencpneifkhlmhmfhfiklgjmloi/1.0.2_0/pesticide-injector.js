(function(window, document){

  'use strict';

  // inject the pesticide CSS
  function toggleAssets(tab) {
    var injector = '';

    // logic test if the injected assets exists
    injector += 'if (document.getElementById("pesticideCSS")) {';

    //if they exist, remove them
    injector += 'document.getElementsByTagName("head")[0].removeChild(document.getElementById("pesticideCSS"));';

    //if they don't exist, inject them
    injector += '} else {';

    injector += 'pesticideCSS = document.createElement("link");';
    injector += 'pesticideCSS.rel = "stylesheet";';
    injector += 'pesticideCSS.type = "text/css";';
    injector += 'pesticideCSS.href = chrome.extension.getURL("/pesticide.min.css");';
    injector += 'pesticideCSS.id = "pesticideCSS";';
    injector += 'document.getElementsByTagName("head")[0].appendChild(pesticideCSS);';

    //close logic test
    injector += '}';

    chrome.tabs.executeScript({code: injector});
  }

  chrome.browserAction.onClicked.addListener(function(tab){
    toggleAssets(tab);
  });

}(window, document));
