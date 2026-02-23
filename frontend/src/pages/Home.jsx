import { Box, Heading, Text, Button } from '@chakra-ui/react'
import { Link } from 'react-router-dom'

function Home() {
  return (
    <Box maxW="600px" mx="auto" mt="10" p="6" textAlign="center">
      <Heading size="2xl" mb="4">Flask-React Boilerplate</Heading>
      <Text mb="6">Welcome to the Flask-React Boilerplate platform.</Text>
      <Button asChild>
        <Link to="/status">Backend Status</Link>
      </Button>
    </Box>
  )
}

export default Home
