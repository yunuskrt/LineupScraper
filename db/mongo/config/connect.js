const { MongoClient } = require('mongodb')

async function connectToDatabase(uri) {
	const client = new MongoClient(uri)
	try {
		// Connect the client to the server
		await client.connect()
		console.log('Connected to MongoDB Atlas successfully')

		// Return the client to be used elsewhere
		return client
	} catch (error) {
		console.error('Error connecting to MongoDB Atlas:', error)
		process.exit(1) // Exit process if connection fails
	}
}

module.exports = connectToDatabase
