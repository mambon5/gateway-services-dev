
const hostname = '127.0.0.1';
const port = 3000;

//mqtt clients:

var mqtt=require('mqtt');

broker="127.0.0.1"
porto=1883
user="roma_masana"
passw="all_I_want_for_christmas_is_you"

url = "mqtt://"+broker + ":" + porto
/** This is a description of the foo function. */
function foo() {
}

options={
  clientId:"Node-JS publisher",
  username:user,
  password:passw,
  clean:true};

var client = mqtt.connect(url,options)

/**
 * on connect to MQTT broker function, store some information in the protocol buffer format, in the variable **buf**
 *  
 *
 * @param [num]
 * @param [str]
 * @param [bool]
 * @param [nil]
 */
client.on("connect",function(){	
  console.log("connected");
  topic = "cl-req/n/145"
  client.subscribe(topic, function() {
    console.log(`Subscribed to topic '${topic}'`)
  })

  // publishing a message:

  // we will use buffer format for encoding an array of integers into an array of bytes: https://nodejs.org/api/buffer.html
  var buf = new Buffer.alloc(16,0)       // crea un buffer per posar bytes, i els inicialitza tots en 0. 

  // empaqueta de int a bytes:
  buf.writeUInt8(3,2)                         // B posa un byte(Int8) amb valor "2" al tercer byte del array (podria ser el message type)
  buf.writeInt8(65,3)                         // b guarda 1 byte signed a la posició 4 del array
  buf.writeInt16LE(2110,0)                    // h little endian codes 2 bytes signed amb valor 2110 al primer i segon byte del array, podria ser message id
  buf.writeUInt16LE(2110,0)                   // H little endian codes 2 bytes unsigned amb valor 2110 al primer i segon byte del array, podria ser message id
  buf.writeInt32LE(-1023,4)                   // i guarda 4 signed bytes a la posició 5-8 del array
  buf.writeUInt32LE(3023,4)                   // I guarda 4 unsigned bytes a la posició 5-8 del array
  buf.writeBigInt64LE( BigInt(-98988) , 8)    // q guarda 8 signed bytes a la posicio 10-18
  buf.writeBigUInt64LE( BigInt(432988) , 8)   // Q guarda 8 Unsigned bytes a la posicio 10-18

  client.publish(topic, buf)
  console.log("message sent!:");
  console.log(buf)
})


/**
 * on message received function, red the information contained in the payload, by passing from bytes to int using the protocol buffer format
 *  
 *
 * @param [num]
 * @param [str]
 * @param [bool]
 * @param [nil]
 */
client.on("message", function(topic, payload){
  /** whatever */
  // getting a message:
  console.log("message received on topic: " + topic + "!")
  console.log(payload)
  buf = payload
  // desempaqueta els bytes a int
  console.log("message description:")
  console.log(buf.readUInt8(2)    )               // B posa un byte(Int8) amb valor "2" al tercer byte del array (podria ser el message type))
  console.log(buf.readInt8(3) )                   // b guarda 1 byte signed a la posició 4 del array
  console.log(buf.readInt16LE(0)           )      // h little endian codes 2 bytes signed amb valor 2110 al primer i segon byte del array, podria ser message id
  console.log(buf.readUInt16LE(0)          )      // H little endian codes 2 bytes unsigned amb valor 2110 al primer i segon byte del array, podria ser message id
  console.log(buf.readInt32LE(4)           )      // i guarda 4 signed bytes a la posició 5-8 del array
  console.log(buf.readUInt32LE(4)          )      // I guarda 4 unsigned bytes a la posició 5-8 del array
  console.log(Number( buf.readBigInt64LE(8)  )  ) // q guarda 8 signed bytes a la posicio 10-18
  console.log(Number( buf.readBigUInt64LE(8) ) )  // Q guarda 8 Unsigned bytes a la posicio 10-18
  console.log("message payload:")
  console.log(buf)

  
})