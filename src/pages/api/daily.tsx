// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

const ObjectId = require("mongodb").ObjectId

const { connectToDatabase } = require("../../middleware/database")

export default async function handler(req, res) {
  // switch the methods
  switch (req.method) {
    case "GET": {
      return getPosts(req, res)
    }
  }
}

// Getting all posts.
async function getPosts(req, res) {
  try {
    let { db } = await connectToDatabase()
    let posts = await db.collection("games_today").find({}).toArray()
    return res.json({
      message: JSON.parse(JSON.stringify(posts)),
      success: true,
    })
  } catch (error) {
    return res.json({
      message: new Error(error).message,
      success: false,
    })
  }
}
