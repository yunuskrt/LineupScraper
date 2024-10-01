const fs = require('fs')
const { ObjectId } = require('mongodb')
const connectToDatabase = require('./config/connect')
require('dotenv').config()

const insert = async (client, dbName, collectionName, data) => {
	// construct collection
	const db = client.db(dbName)
	const collection = db.collection(collectionName)
	// insert data into collection
	const result = await collection.insertMany(data)
	console.log(`${result.insertedCount} documents were inserted`)
}
const read = async (client, dbName, collectionName) => {
	// construct collection
	const db = client.db(dbName)
	const collection = db.collection(collectionName)
	// read data from collection
	const cursor = await collection.find({})
	// return all the documents
	return cursor.toArray()
}
const insertFromFileToMongoDB = async (path, dbName, collectionName) => {
	const client = await connectToDatabase(process.env.MONGO_URI)
	try {
		fs.readFile(path, 'utf8', async (err, data) => {
			if (err) {
				console.log(err)
			} else {
				try {
					// read data from file
					const parsedData = JSON.parse(data)
					// insert data into MongoDB
					await insert(client, dbName, collectionName, parsedData)
				} catch (error) {
					console.error('Error inserting data into MongoDB:', error)
				} finally {
					// close the connection
					await client.close()
				}
			}
		})
	} catch (error) {
		console.error('Unexpected error:', error)
		await client.close()
	}
}

const insertMatches = async () => {
	const client = await connectToDatabase(process.env.MONGO_URI)

	idMapping = {}
	// construct manager id mapping
	managersData = await read(client, 'lineup', 'managers')
	managersData.forEach((manager) => {
		idMapping[manager['id']] = manager['_id'].toString()
	})
	// construct team id mapping
	teamsData = await read(client, 'lineup', 'teams')
	teamsData.forEach((team) => {
		idMapping[team['id']] = team['_id'].toString()
	})
	// construct player id mapping
	playersData = await read(client, 'lineup', 'players')
	playersData.forEach((player) => {
		idMapping[player['id']] = player['_id'].toString()
	})
	// read matches data
	try {
		fs.readFile('./data/matches.json', 'utf8', async (err, data) => {
			if (err) {
				console.log(err)
			} else {
				try {
					// read data from file
					const parsedData = JSON.parse(data)
					// firstItem = parsedData[0]
					// console.log(Object.keys(firstItem))
					// console.log(Object.keys(firstItem['home']))
					// console.log(Object.keys(firstItem['home']['first11'][0]))

					const formattedData = parsedData.map((match) => {
						return {
							type: match['type'],
							league: match['league'],
							country: match['country'],
							season: match['season'],
							round: match['round'],
							date: match['date'],
							stadium: match['stadium'],
							attendance: match['attendance'],
							referee: match['referee'],
							extraTime: match['extraTime'],
							penalty: match['penalty'],
							home: {
								id: new ObjectId(idMapping[match['home']['id']]),
								position: match['home']['position'],
								score: match['home']['score'],
								halfScore: match['home']['halfScore'],
								lineup: match['home']['lineup'],
								manager: new ObjectId(idMapping[match['home']['manager']]),
								first11: match['home']['first11'].map((player) => {
									return {
										id: new ObjectId(idMapping[player['id']]),
										number: player['number'],
										position: player['position'],
										actions: player['actions'],
									}
								}),
								substitutes: match['home']['substitutes'].map((player) => {
									return {
										id: new ObjectId(idMapping[player['id']]),
										number: player['number'],
										position: player['position'],
										actions: player['actions'],
									}
								}),
							},
							away: {
								id: new ObjectId(idMapping[match['away']['id']]),
								position: match['away']['position'],
								score: match['away']['score'],
								halfScore: match['away']['halfScore'],
								lineup: match['away']['lineup'],
								manager: new ObjectId(idMapping[match['away']['manager']]),
								first11: match['away']['first11'].map((player) => {
									return {
										id: new ObjectId(idMapping[player['id']]),
										number: player['number'],
										position: player['position'],
										actions: player['actions'],
									}
								}),
								substitutes: match['away']['substitutes'].map((player) => {
									return {
										id: new ObjectId(idMapping[player['id']]),
										number: player['number'],
										position: player['position'],
										actions: player['actions'],
									}
								}),
							},
						}
					})

					// insert matches into mongoDB
					console.log('Parsed data length', parsedData.length)
					await insert(client, 'lineup', 'matches', formattedData)
				} catch (error) {
					console.error('Error inserting data into MongoDB:', error)
				}
			}
		})
	} catch (error) {
		console.error('Unexpected error:', error)
		await client.close()
	}

	console.log(Object.keys(idMapping).length)
}

const deleteIdField = async (dbName, collectionName) => {
	const client = await connectToDatabase(process.env.MONGO_URI) // Connect to MongoDB Atlas
	try {
		const db = client.db(dbName)
		const collection = db.collection(collectionName)

		// Remove the 'name' field from all documents
		const result = await collection.updateMany({}, { $unset: { id: '' } })
		console.log(
			`${result.modifiedCount} documents were updated to remove the 'id' field.`
		)
	} catch (error) {
		console.error('Error updating documents in MongoDB:', error)
	} finally {
		await client.close() // Close the MongoDB connection
	}
}

const start = async () => {
	const client = await connectToDatabase(process.env.MONGO_URI)
}

start()
