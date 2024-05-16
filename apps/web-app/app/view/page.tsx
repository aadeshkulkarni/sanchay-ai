//@ts-nocheck
"use client";

import { useEffect, useState } from "react";
import { Button } from "../components/ui/button";
import { ResultDialog } from "../components/ResultDialog";

export interface video {
	_id: string;
	title: string;
}
export default function Home() {
	const [videos, setVideos] = useState<any>([]);
	const [output, setOutput] = useState<string>("");
	const [activePreview, setActivePreview] = useState<any>({});
	useEffect(() => {
		async function fetchVideos() {
			const res = await fetch("./api/videos");
			const data = await res.json();
			setVideos(data.data);
		}
		fetchVideos();
	}, []);
	useEffect(() => {
		console.log("Videos: ", videos);
	}, [videos]);

	function openDialog(data) {
		setDialogOpen(true);
		setOutput(data);
	}

	return (
		<main className="w-screen h-screen grid grid-cols-12 p-4 gap-8">
			<div className="col-span-6 flex flex-col justify-start items-center p-4">
				<h1 className="py-8 text-lg font-bold">Video list</h1>
				<div className="flex gap-8 flex-wrap justify-center">
					{videos.length > 0 &&
						videos?.map((video: video) =>
							video.failed ? (
								<ErrorCard key={video._id} video={video} />
							) : (
								<SuccessCard setOutput={setOutput} key={video._id} video={video} />
							)
						)}
				</div>
			</div>
			<div className="col-span-6 flex flex-col justify-start items-center p-4">
				<h1 className="py-8 text-lg font-bold">Preview</h1>
				<div>{output}</div>
			</div>
		</main>
	);
}

const ErrorCard = ({ video }) => (
	<div key={video._id} className="relative border p-8 min-w-full min-h-[100px]">
		<div className="border-b font-bold pb-2 tracking-wide">{video.title}</div>
		<div className="p-4 flex justify-center items-center h-full">{video.error}</div>
		<div className="absolute top-4 right-6 px-4 py-2 rounded-full bg-red-400 text-white">
			Failed
		</div>
	</div>
);

const SuccessCard = ({ video, setOutput }) => (
	<div key={video._id} className="relative border p-8 min-w-full min-h-[100px]">
		<div className="border-b font-bold pb-2 tracking-wide">{video.title}</div>
		<div className="p-4 h-full flex gap-4 justify-center items-center w-full">
			<div>
				<video width="300" height="300" controls>
					<source src={video.videoUrl} type="video/mp4" />
					Your browser does not support the video tag.
				</video>
			</div>
			<div className="flex flex-col justify-center items-center gap-4">
				<Button size="sm" className="w-[160px]" onClick={() => setOutput(video.captions)}>
					Captions
				</Button>
				<Button size="sm" className="w-[160px]" onClick={() => setOutput(video.transcription)}>
					Transcription
				</Button>
				<Button size="sm" className="w-[160px]" onClick={() => setOutput(video.chapters)}>
					Chapters
				</Button>
			</div>
		</div>
		<div className="absolute top-4 right-6 px-4 py-2 rounded-full bg-green-200 border">Success</div>
	</div>
);
