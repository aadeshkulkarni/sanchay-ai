import amqp from 'amqplib'

const RABBITMQ = process.env.RABBITMQ_DEV 

async function executeInBackground(queue:any, payload:any) {
  const connection = await amqp.connect(RABBITMQ);
  const channel = await connection.createChannel();
  await channel.assertQueue(queue, { durable: false });
  channel.sendToQueue(queue, Buffer.from(JSON.stringify(payload)));
}

export default executeInBackground