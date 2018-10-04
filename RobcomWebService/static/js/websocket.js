/**
 * Create a WebSocket connection.
 * @param {string} p_address - server address.
 * @param {int} p_port - server port.
 * @param {function} p_onOpen - On connection open callback.
 * @param {function} p_onMessage - On connection receive callback.
 * @param {function} p_onClose - On connection close callback.
 * @param {function} p_onError - On connection error callback.
 */
function createWebSocket(p_address, p_port, p_onOpen, p_onMessage, p_onClose, p_onError) {
	if(typeof p_address == 'undefined' || p_address == null) {
		return;
	}

	var v_port = 80;

	if(p_port != null && typeof p_port == 'number') {
		v_port = p_port;
	}

	var v_connection = new WebSocket(p_address + ':' + v_port + '/wss');

	if(p_onOpen != null && typeof p_onOpen == 'function') {
		v_connection.onopen = p_onOpen;
	}

	if(p_onMessage != null && typeof p_onMessage == 'function') {

		v_connection.onmessage = (function() {

			return function(e) {

				var v_message = JSON.parse(e.data);
				var v_context = null;

				if (v_message.v_context_code!=0 && v_message.v_context_code!=null) {

					for (var i=0; i<v_connection.contextList.length; i++) {

						if (v_connection.contextList[i].code == v_message.v_context_code) {
							v_context = v_connection.contextList[i].context;
							v_connection.contextList.splice(i,1);
							break;
						}

					}

				}

				p_onMessage(v_message,v_context);

			}
		})();
	}

	if(p_onClose != null && typeof p_onClose == 'function') {
		v_connection.onclose = p_onClose;
	}

	if(p_onError != null && typeof p_onError == 'function') {
		v_connection.onerror = p_onError;
	}

	v_connection.contextList = [];
	v_connection.contextCode = 1;

	return v_connection;
}

/// <summary>
/// Sends a message through the websocket connection to the server.
/// </summary>
/// <param name="p_connection">The websocket object that corresponds to the connection.</param>
/// <param name="p_messageCode">Transaction code that identify the operation.</param>
/// <param name="p_messageData">A object that will be send to the server.</param>
/// <param name="p_error">If it's an error message.</param>
/// <param name="p_context">The message context object. Anything that would be used when client receives a response message related to this request.</param>
function sendWebSocketMessage(p_connection, p_messageCode, p_messageData, p_error, p_context) {
	waitForSocketConnection(
		p_connection,
		function() {

			var v_context_code = 0;

			//Configuring context
			if (p_context!=null) {
				p_connection.contextCode += 1;
				v_context_code = p_connection.contextCode;
				var v_context = {
					code: v_context_code,
					context: p_context
				}
				p_connection.contextList.push(v_context);
			}


			p_connection.send(
				JSON.stringify({
					v_code: p_messageCode,
					v_context_code: v_context_code,
					v_error: p_error,
					v_data: p_messageData
				})
			);
		}
	);
}

/// <summary>
/// Do something when the connection is opened
/// </summary>
/// <param name="p_connection">The websocket object that corresponds to the connection.</param>
/// <param name="p_callback">The callback that contains somenthing to be done.</param>
function waitForSocketConnection(p_connection, p_callback){
	setTimeout(
		function () {
			if (p_connection.readyState == 1) {
				if(p_callback != null) {
					p_callback();
				}

				return;
			}
			else {
				waitForSocketConnection(p_connection, p_callback);
			}
		},
		5
	);
}
