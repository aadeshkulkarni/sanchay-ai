import { Video } from './db/model'
import { uploadToS3 } from '@/utils/fileUpload'
import executeInBackground from '@/app/worker/worker'

const create = async (formData: FormData) => {
    'use server'
    console.log('dump')
    const title = formData.get('title')
    const file = formData.get('video') as File
    // TODOS: add file type = video check here
    if (!file.size || !title) {
        return
    }

    const videoUrl = await uploadToS3(file)
    const video = await Video.create({ title: title, videoUrl: videoUrl })
    const newVideo = await video.save()
    await executeInBackground('task_queue', { ...newVideo })
}

export default function Home() {
    return (
        <main className='w-screen h-screen flex justify-center items-center'>
            <form action={create} className='p-4 border border-black flex flex-col gap-4'>
                <input name='title' type='text' placeholder='Title' className='border py-2 px-3' />
                <input name='video' type='file' />
                <button className='bg-black p-2 text-white rounded-md'>Process</button>
            </form>
        </main>
    )
}
