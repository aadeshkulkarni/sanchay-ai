import AWS from 'aws-sdk'
import { v4 as uuidv4 } from 'uuid'

console.log('Process ENV: ', process.env)
const s3 = new AWS.S3({
    endpoint: 'http://localhost:4566',
    s3ForcePathStyle: true,
    accessKeyId: "NA",
    secretAccessKey: "NA",
    region: "ap-south-1"
})
const BUCKET_NAME = process.env.S3_BUCKET_NAME
s3.api.globalEndpoint = 's3.localhost.localstack.cloud'

async function createBucketIfNotExists() {
    try {
        var params = {
            Bucket: BUCKET_NAME
        }
        const data = await s3.waitFor('bucketNotExists', params)
        console.log("2")
        console.log("Data from createBucket(): ",data)
    } catch (ex) {
        console.log("2 - Error:")
        console.log(ex)
    }
}

export const uploadToS3 = async (file) => {
    try {
        console.log("1")
        await createBucketIfNotExists()
        console.log("3 - bucket passed")
        const fileExtension = file.name.split('.').pop()
        const arrayBuffer = await file.arrayBuffer()
        const buffer = new Uint8Array(arrayBuffer)
        const params = {
            Bucket: BUCKET_NAME,
            Key: `${uuidv4()}.${fileExtension}`,
            Body: buffer
        }
        console.log("4 - params: ",params)
        const data = await s3.upload(params).promise()
        console.log("5 - data from upload: ",data)
        return data['Location']
    } catch (ex) {
        console.error('Error uploading file:', ex)
        return false
    }
}
