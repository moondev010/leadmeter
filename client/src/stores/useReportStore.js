import { create } from "zustand";

const useReportStore = create((set) => ({
    claim: '',
    report: {},
    setClaim: (v) => set({ claim: v }),
    setReport: (v) => set({ report: v })
}))

export default useReportStore