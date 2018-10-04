/**
 * Transaction codes of client requests.
 */
var gv_request = {
    Login: '0',
    ApplyRegister: '1'
};

/**
 * Transaction codes of server responses.
 */
var gv_response = {
    LoginResult: '0',
    AppliedRegister: '1'
};

/**
 * The variable that will receive the WebSocket object.
 */
var gv_hotpostWebSocket;

/**
 * Start hotspot websocket client
 * @param {int} p_port - port where websocket client will connect.
 */
function startHotspotWebSocket(p_port) {
	gv_hotpostWebSocket  = createWebSocket(
		'wss://' + window.location.hostname,
		p_port,
		function(p_event) {//Open
			hotspotLogin();
		},
		function(p_message, p_context) {//Message
			console.log(p_message);
			console.log(p_context);

			if(p_message.v_error) {
				alert('Uma mensagem de erro foi recebida do servidor: <br>' + p_message.v_data);
				return;
			}

			switch(p_message.v_code) {
				case gv_response.LoginResult: {
					hotspotLoginResult(p_message.v_data);
					break;
				}
                case gv_response.AppliedRegister: {
					hotspotAppliedRegister(p_message.v_data);
					break;
				}
			}
		},
		function(p_event) {//Close
			alert(p_event);
		},
		function(p_event) {//Error
			alert(p_event);
		}
	);
}

/**
 * Executed on page load.
 */
$(document).ready(function() {
    //Open a new connection with the websocket server
    startHotspotWebSocket(WEBSOCKET_PORTS.HOTSPOT);
});

/**
 * Sends a login message to server.
 */
function hotspotLogin() {
    sendWebSocketMessage(gv_hotpostWebSocket, gv_request.Login, null, false);
}

/**
 * Sends a apply register message to server.
 * @param {object} p_data - javascript object with the following structure: {name, phone, email, cep}.
 */
function hotspotApplyRegister(p_data) {
    sendWebSocketMessage(gv_hotpostWebSocket, gv_request.ApplyRegister, p_data, false);
}

/**
 * Handles login result message received from the server.
 * @param {object} p_data - javascript object returned from the server.
 */
function hotspotLoginResult(p_data) {
//    alert('Estou habilitado?: ' + p_data.allowed);

    //If user can navigate, redirect from portal to google.
    if(p_data.allowed) {
        window.location = 'https://www.google.com';
    }
    else {
//        alert('Por favor, realize seu cadastro.');
    }
}

/**
 * Handles applied register message received from the server.
 * @param {object} p_data - javascript object returned from the server.
 */
function hotspotAppliedRegister(p_data) {
//    alert('Estou habilitado?: ' + p_data.allowed);

    //If user can navigate, redirect from portal to google.
    if(p_data.allowed) {
        window.location = 'https://www.google.com';
    }
    else {
        alert('Por favor, realize seu cadastro.');
    }
}
