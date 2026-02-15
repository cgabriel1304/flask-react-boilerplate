import { Box, Heading, Text, Button } from '@chakra-ui/react'
import { Link } from 'react-router-dom'

function Home() {
  return (
    <Box maxW="600px" mx="auto" mt="10" p="6" textAlign="center">
      <Heading size="2xl" mb="4">Cyberitance</Heading>
      <Text mb="6">Welcome to the Cyberitance platform.</Text>
      <Button asChild>
        <Link to="/status">Backend Status</Link>
      </Button>
    </Box>
  )
}

export default Home
