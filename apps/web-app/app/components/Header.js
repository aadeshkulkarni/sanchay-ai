import Link from 'next/link'

const Header = () => {
  return (
    <div className="w-screen bg-black text-white p-4 flex justify-start gap-8 items-center px-8">
        <Link href="/"><h1 className="text-2xl">Sanchay.ai</h1></Link>
        <Link href='/view' className="underline">Your videos</Link>
    </div>
  )
}

export default Header