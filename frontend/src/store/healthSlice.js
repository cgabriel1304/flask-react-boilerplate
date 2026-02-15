import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'

export const fetchHealth = createAsyncThunk('health/fetch', async () => {
  const response = await fetch('/api/health')
  if (!response.ok) {
    throw new Error(`Server responded with ${response.status}`)
  }
  return response.json()
})

const healthSlice = createSlice({
  name: 'health',
  initialState: {
    data: null,
    loading: false,
    error: null,
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchHealth.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchHealth.fulfilled, (state, action) => {
        state.loading = false
        state.data = action.payload
      })
      .addCase(fetchHealth.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
  },
})

export default healthSlice.reducer
