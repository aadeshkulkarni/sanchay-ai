import mongoose from "mongoose";

const MONGODB_URL = process.env.MONGO_DB;
console.log("Aadesh: ",MONGODB_URL)

mongoose.connect(MONGODB_URL);

const videoSchema = new mongoose.Schema({
  videoUrl: String,
  transcription: String,
  subtitles: String,
  chapters: String,
  title: String,
  description: String,
});

const Video = mongoose.models.Video || mongoose.model("Video", videoSchema);

export { Video };
