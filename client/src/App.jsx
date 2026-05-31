import './app.css'

import { useState } from 'react'

import { Route, Switch } from 'wouter'
import { create } from 'zustand'

import ClaimForm from './routes/ClaimForm'
import Report from './routes/Report'
import ReportTest from './routes/ReportTest'

function App() {
  return (
    <main className='w-full flex justify-center'>
      <div className='w-full max-w-2xl'>
        <Switch>
          <Route path='/' component={ClaimForm} />
          <Route path='/report' component={Report} />
          <Route path='/report-test' component={ReportTest} />
        </Switch>
      </div>
    </main>
  )
}

export default App
