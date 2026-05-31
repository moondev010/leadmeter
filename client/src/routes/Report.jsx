import { useState } from "react"

import useReportStore from "../stores/useReportStore"

import Path from "../components/Path"


function Report() {
    const claim = useReportStore((s) => s.claim)
    const report = useReportStore((s) => s.report)

    useState(() => {
        console.log(report)
    }, [])

    if (report !== {}) return (
        <div className='h-dvh flex flex-col py-11 px-5 gap-5'>
            {/*<p>{claim}</p>*/}
            <div className='flex flex-col items-center'>
                <Path percentage={report.score} />
                <p className='text-5xl font-serif font-bold text-green-600'>{report.score}%</p>
                <p className='text-2xl font-serif font-bold text-gray-800 mt-2' >{report.message}</p>
            </div>
            <h1 className="text-2xl font-serif font-bold text-gray-800 mt-2">Here's why</h1>
            <p className='p-3 rounded-md border-2 border-gray-300'>{report.reason}</p>
            <h1 className="text-2xl font-serif font-bold text-gray-800 mt-2">How sure we are?</h1>
            <p className='text-5xl font-serif font-bold text-gray-600 mt-2 w-full text-center'>{report.confidence}%</p>
        </div>
    )
    return <h1>There's nothing here to see</h1>
}

export default Report