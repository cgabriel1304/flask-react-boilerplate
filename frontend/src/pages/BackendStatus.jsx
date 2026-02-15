import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Box, Heading, Text, Button, Spinner } from '@chakra-ui/react'
import { Link } from 'react-router-dom'
import { fetchHealth } from '../store/healthSlice'

function BackendStatus() {
  const dispatch = useDispatch()
  const { data, loading, error } = useSelector((state) => state.health)

  useEffect(() => {
    dispatch(fetchHealth())
  }, [dispatch])

  return (
    <Box maxW="600px" mx="auto" mt="10" p="6" textAlign="center">
      <Heading size="2xl" mb="6">Backend Status</Heading>

      {loading && <Spinner size="xl" />}

      {error && (
        <Text color="red.500" mb="4">Error: {error}</Text>
      )}

      {data && (
        <Box mb="6">
          <Text fontSize="lg">
            Status: <strong>{data.status}</strong>
          </Text>
          <Text fontSize="lg">
            Message: <strong>{data.message}</strong>
          </Text>
        </Box>
      )}

      <Box display="flex" gap="4" justifyContent="center">
        <Button onClick={() => dispatch(fetchHealth())}>Refresh</Button>
        <Button variant="outline" asChild>
          <Link to="/">Back to Home</Link>
        </Button>
      </Box>
    </Box>
  )
}

export default BackendStatus
