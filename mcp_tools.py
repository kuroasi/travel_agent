"""
MCP (Model Control Protocol) Tools for Travel Agent
This module provides tools to interact with MCP servers like mcp-server-airbnb.
"""

import os
import json
import requests
import subprocess
import time
import signal
import atexit
from typing import Dict, List, Optional, Any, Union
import logging
from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Default MCP configuration
DEFAULT_MCP_CONFIG = {
    "mcpServers": {
        "airbnb": {
            "command": "npx",
            "args": [
                "-y",
                "@openbnb/mcp-server-airbnb"
            ]
        }
    }
}

# MCP Server management
class MCPServerManager:
    """Manages MCP server processes."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the MCP Server Manager.
        
        Args:
            config_path: Path to the MCP configuration JSON file. If None, uses default config.
        """
        self.config = self._load_config(config_path)
        self.processes: Dict[str, subprocess.Popen] = {}
        self.ports: Dict[str, int] = {}
        self.base_port = 8080
        
        # Register cleanup on exit
        atexit.register(self.stop_all_servers)
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load MCP configuration from file or use default."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return DEFAULT_MCP_CONFIG
    
    def start_server(self, server_name: str) -> int:
        """
        Start an MCP server by name.
        
        Args:
            server_name: Name of the server as defined in the config
            
        Returns:
            Port number the server is running on
        
        Raises:
            ValueError: If server_name is not in the configuration
        """
        if server_name not in self.config["mcpServers"]:
            raise ValueError(f"Server '{server_name}' not found in MCP configuration")
        
        # If server is already running, return its port
        if server_name in self.processes and self.processes[server_name].poll() is None:
            return self.ports[server_name]
        
        # Assign a port
        port = self.base_port + len(self.processes)
        self.ports[server_name] = port
        
        # Get server config
        server_config = self.config["mcpServers"][server_name]
        command = server_config["command"]
        args = server_config["args"]
        
        # Start the server process
        env = os.environ.copy()
        env["PORT"] = str(port)
        
        logger.info(f"Starting MCP server '{server_name}' on port {port}")
        process = subprocess.Popen(
            [command] + args,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        self.processes[server_name] = process
        
        # Wait for server to start
        time.sleep(2)  # Simple wait, could be improved with actual health check
        
        if process.poll() is not None:
            # Process exited prematurely
            stdout, stderr = process.communicate()
            logger.error(f"Server '{server_name}' failed to start: {stderr}")
            raise RuntimeError(f"Failed to start MCP server '{server_name}': {stderr}")
        
        logger.info(f"MCP server '{server_name}' started successfully on port {port}")
        return port
    
    def stop_server(self, server_name: str) -> None:
        """Stop a specific MCP server."""
        if server_name in self.processes:
            process = self.processes[server_name]
            if process.poll() is None:  # Process is still running
                logger.info(f"Stopping MCP server '{server_name}'")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
            
            del self.processes[server_name]
            if server_name in self.ports:
                del self.ports[server_name]
    
    def stop_all_servers(self) -> None:
        """Stop all running MCP servers."""
        for server_name in list(self.processes.keys()):
            self.stop_server(server_name)

# Create a singleton instance of the MCP Server Manager
mcp_manager = MCPServerManager()

# Input/Output models for the Airbnb search tool
class AirbnbSearchInput(BaseModel):
    location: str = Field(..., description="Location to search for listings (city, address, etc.)")
    check_in: str = Field(..., description="Check-in date in YYYY-MM-DD format")
    check_out: str = Field(..., description="Check-out date in YYYY-MM-DD format")
    adults: int = Field(2, description="Number of adults")
    children: int = Field(0, description="Number of children")
    infants: int = Field(0, description="Number of infants")
    pets: int = Field(0, description="Number of pets")
    price_min: Optional[int] = Field(None, description="Minimum price per night")
    price_max: Optional[int] = Field(None, description="Maximum price per night")

@tool("airbnb_search", args_schema=AirbnbSearchInput)
def airbnb_search(
    location: str,
    check_in: str,
    check_out: str,
    adults: int = 2,
    children: int = 0,
    infants: int = 0,
    pets: int = 0,
    price_min: Optional[int] = None,
    price_max: Optional[int] = None
) -> str:
    """
    Search for Airbnb listings based on location, dates, and guests.
    
    Args:
        location: Location to search for listings (city, address, etc.)
        check_in: Check-in date in YYYY-MM-DD format
        check_out: Check-out date in YYYY-MM-DD format
        adults: Number of adults
        children: Number of children
        infants: Number of infants
        pets: Number of pets
        price_min: Minimum price per night
        price_max: Maximum price per night
        
    Returns:
        JSON string with search results
    """
    try:
        # Start the Airbnb MCP server
        port = mcp_manager.start_server("airbnb")
        
        # Prepare the search parameters
        params = {
            "location": location,
            "checkIn": check_in,
            "checkOut": check_out,
            "adults": adults,
            "children": children,
            "infants": infants,
            "pets": pets
        }
        
        # Add optional parameters if provided
        if price_min is not None:
            params["priceMin"] = price_min
        if price_max is not None:
            params["priceMax"] = price_max
        
        # Make the request to the MCP server
        response = requests.get(f"http://localhost:{port}/api/search", params=params)
        response.raise_for_status()
        
        # Process the response
        results = response.json()
        
        # Format the results for better readability
        formatted_results = []
        for listing in results.get("listings", [])[:5]:  # Limit to 5 listings for brevity
            formatted_results.append({
                "id": listing.get("id"),
                "name": listing.get("name"),
                "url": listing.get("url"),
                "price": listing.get("price"),
                "rating": listing.get("rating"),
                "reviewCount": listing.get("reviewCount"),
                "location": listing.get("location"),
                "roomType": listing.get("roomType")
            })
        
        return json.dumps({"listings": formatted_results}, indent=2)
    
    except Exception as e:
        logger.error(f"Error in Airbnb search: {str(e)}")
        return f"Error searching Airbnb: {str(e)}"

# Input model for the Airbnb listing details tool
class AirbnbListingInput(BaseModel):
    listing_id: str = Field(..., description="Airbnb listing ID")

@tool("airbnb_listing_details", args_schema=AirbnbListingInput)
def airbnb_listing_details(listing_id: str) -> str:
    """
    Get detailed information about a specific Airbnb listing.
    
    Args:
        listing_id: Airbnb listing ID
        
    Returns:
        JSON string with listing details
    """
    try:
        # Start the Airbnb MCP server
        port = mcp_manager.start_server("airbnb")
        
        # Make the request to the MCP server
        response = requests.get(f"http://localhost:{port}/api/listings/{listing_id}")
        response.raise_for_status()
        
        # Return the listing details
        return json.dumps(response.json(), indent=2)
    
    except Exception as e:
        logger.error(f"Error getting Airbnb listing details: {str(e)}")
        return f"Error getting listing details: {str(e)}"

# Function to get all available MCP tools
def get_mcp_tools() -> List:
    """Return a list of all MCP tools."""
    return [airbnb_search, airbnb_listing_details]

# If this module is run directly, test the MCP server
if __name__ == "__main__":
    try:
        # Test starting the Airbnb MCP server
        port = mcp_manager.start_server("airbnb")
        print(f"Airbnb MCP server started on port {port}")
        
        # Keep the server running for manual testing
        print("Press Ctrl+C to stop the server...")
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Stopping servers...")
    
    finally:
        # Clean up
        mcp_manager.stop_all_servers()
        print("All servers stopped.")
