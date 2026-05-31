import { useState, useEffect } from 'react'
import '../css/path.css'

function Path({ percentage }) {
    useEffect(() => {
        function setPercentage(percentage, duration) {
            duration = duration * (1 + percentage)

            const path = document.querySelector(".path-indc");
            const length = path.getTotalLength();

            console.log(length)

            path.style.strokeDasharray = length;
            path.style.strokeDashoffset = length;

            path.animate([{ strokeDashoffset: `${(1 - percentage) * length}` }],
                {
                    duration: duration,
                    iterations: 1,
                    fill: "forwards",
                    easing: "ease-out"
                }
            )

            if (percentage === 0) return

            const circle = document.querySelector(".circle");

            circle.animate([{ offsetDistance: `${percentage * 100}%` }],
                {
                    duration: duration,
                    iterations: 1,
                    fill: "forwards",
                    easing: "ease-out"
                }
            )
        }

        setPercentage(percentage / 100, 800)
    }, [])

    return (
        <>
            <svg width="24" height="24" version="1.1" viewBox="0 0 6.35 6.35" xmlns="http://www.w3.org/2000/svg" class="path">
                <path
                    d="m0.79375 4.4979s1.0583-1.8521 1.5875-1.8521c0.52917 0 1.0583 0.79378 1.5875 0.79375 0.52917-3.35e-5 1.5875-1.8521 1.5875-1.8521"
                    fill="none" stroke="#000" stroke-linecap="round" stroke-width=".13229" class="path-indc stroke-green-600" />
                <circle cx=".39687" cy=".39687" r=".39687" class="circle fill-green-600" />
                <path
                    d="m0.79375 4.4979s1.0583-1.8521 1.5875-1.8521c0.52917 0 1.0583 0.79378 1.5875 0.79375 0.52917-3.35e-5 1.5875-1.8521 1.5875-1.8521"
                    fill="none" stroke="#000" stroke-linecap="round" stroke-width=".26458" class="path-main stroke-green-600/20" />
            </svg>
        </>

    )
}

export default Path