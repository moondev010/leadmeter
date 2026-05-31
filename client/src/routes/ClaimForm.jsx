import { useState, useEffect } from "react"

import { useLocation } from "wouter";

import useReportStore from "../stores/useReportStore"

function ClaimForm() {
    const [location, navigate] = useLocation()

    const [tmpClaim, setTmpClaim] = useState('')

    const setClaim = useReportStore((s) => s.setClaim)
    const setReport = useReportStore((s) => s.setReport)

    const claim = useReportStore((s) => s.claim)

    const apiUrl = 'http://192.168.1.76:5000/'

    const fetchAndRedirect = async () => {
        try {
            setClaim(tmpClaim)

            const response = await fetch(apiUrl, {
                method: 'POST',
                body: JSON.stringify({ claim: tmpClaim }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })

            if (!response.ok) {
                console.log(`Response status: ${response.status}`);
            }

            const result = await response.json();
            console.log(result);

            setReport(result)

            navigate('/report')
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <div className="h-dvh flex flex-col justify-center py-11 px-5 gap-5">
            <textarea name='claim' onChange={(e) => setTmpClaim(e.target.value)} className='h-36 p-3 rounded-md border-2 border-gray-300 resize-none' placeholder='Type your claims here'></textarea>
            <button onClick={() => fetchAndRedirect()} className="h-14 bg-gray-900 text-gray-50 rounded-md hover:bg-gray-800 active:bg-gray-700 shadow-sm">Send</button>
        </div>
    )
}

export default ClaimForm