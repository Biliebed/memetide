import asyncio
import httpx
from typing import List, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from .models import TokenMention


class TwitterScraper:
    """
    Scrape Twitter/X for crypto mentions
    Uses Nitter (Twitter frontend) to avoid API requirements
    """
    
    # Public Nitter instances (no auth needed)
    NITTER_INSTANCES = [
        "https://nitter.net",
        "https://nitter.privacydev.net",
        "https://nitter.poast.org",
    ]
    
    # Crypto keywords to search
    SEARCH_QUERIES = [
        "memecoin",
        "new token",
        "$100x",
        "gem alert",
        "moonshot",
        "stealth launch",
        "fair launch",
        "presale now",
    ]
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.current_instance = 0
    
    def _get_instance(self) -> str:
        """Get current Nitter instance"""
        return self.NITTER_INSTANCES[self.current_instance % len(self.NITTER_INSTANCES)]
    
    def _rotate_instance(self):
        """Rotate to next instance if one fails"""
        self.current_instance += 1
    
    async def search(self, query: str, limit: int = 50) -> List[TokenMention]:
        """
        Search Twitter for query via Nitter
        """
        mentions = []
        instance = self._get_instance()
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Nitter search URL
                url = f"{instance}/search"
                params = {
                    "f": "tweets",
                    "q": query,
                    "since": "",  # Can add date filter
                }
                
                response = await client.get(url, params=params)
                
                if response.status_code != 200:
                    print(f"[Scraper] Nitter returned {response.status_code}")
                    self._rotate_instance()
                    return mentions
                
                # Parse HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find tweet containers
                tweets = soup.find_all('div', class_='timeline-item')
                
                for tweet in tweets[:limit]:
                    try:
                        # Extract text
                        text_elem = tweet.find('div', class_='tweet-content')
                        if not text_elem:
                            continue
                        
                        text = text_elem.get_text(strip=True)
                        
                        # Extract author
                        author_elem = tweet.find('a', class_='username')
                        author = author_elem.get_text(strip=True) if author_elem else None
                        
                        # Extract stats (likes, RTs)
                        stats = tweet.find_all('span', class_='icon-container')
                        likes = 0
                        retweets = 0
                        
                        for stat in stats:
                            stat_text = stat.get_text(strip=True)
                            if 'retweet' in stat.get('title', '').lower():
                                try:
                                    retweets = int(stat_text.replace(',', ''))
                                except:
                                    pass
                            elif 'like' in stat.get('title', '').lower():
                                try:
                                    likes = int(stat_text.replace(',', ''))
                                except:
                                    pass
                        
                        mention = TokenMention(
                            token_symbol="",  # Will be extracted later
                            timestamp=datetime.utcnow().isoformat(),
                            text=text,
                            author=author,
                            likes=likes,
                            retweets=retweets
                        )
                        
                        mentions.append(mention)
                    
                    except Exception as e:
                        print(f"[Scraper] Error parsing tweet: {e}")
                        continue
                
                print(f"[Scraper] Found {len(mentions)} mentions for '{query}'")
        
        except Exception as e:
            print(f"[Scraper] Error fetching from {instance}: {e}")
            self._rotate_instance()
        
        return mentions
    
    async def scan_all(self) -> List[TokenMention]:
        """
        Scan all crypto keywords
        """
        all_mentions = []
        
        print(f"\n[Scraper] Starting scan across {len(self.SEARCH_QUERIES)} queries...")
        
        for query in self.SEARCH_QUERIES:
            mentions = await self.search(query, limit=30)
            all_mentions.extend(mentions)
            
            # Rate limiting
            await asyncio.sleep(2)
        
        print(f"[Scraper] Scan complete. Total mentions: {len(all_mentions)}")
        
        return all_mentions


class MockTwitterScraper(TwitterScraper):
    """
    Mock scraper for testing without real Twitter data
    """
    
    MOCK_TWEETS = [
        ("$PEPE2 is going to the moon! 🚀 This is the next 100x gem LFG!", "cryptowhale", 234, 89),
        ("Just bought $PEPE2, feeling bullish af, this will moon", "trader_joe", 845, 212),
        ("$PEPE2 chart looking insane rn, breakout incoming!", "moon_boy", 456, 134),
        ("$PEPE2 early gem alert, don't miss this rocket 🔥", "alpha_hunter", 678, 245),
        ("$PEPE2 to 100x ez, based dev, huge potential", "degen_king", 912, 334),
        ("New gem alert: $FLOKI MARS is stealth launching tonight", "gem_finder", 567, 123),
        ("$FLOKI MARS presale is live, don't miss out! 🔥 WAGMI", "crypto_calls", 1890, 634),
        ("FLOKI MARS token about to pump hard, lfg boys", "degen_trader", 734, 167),
        ("$FLOKI MARS bullish af, moon mission started 🚀", "moon_caller", 456, 234),
        ("Guys be careful with $SCAMCOIN, looks like a rug", "crypto_detective", 1234, 456),
        ("$SCAMCOIN contract is sus, avoid this one", "rugwatch", 789, 234),
        ("$SCAMCOIN honeypot confirmed, don't buy", "safu_check", 456, 123),
    ]
    
    async def scan_all(self) -> List[TokenMention]:
        """
        Return mock data for testing
        """
        print(f"\n[MockScraper] Generating mock Twitter data...")
        
        mentions = []
        base_time = datetime.utcnow()
        
        for i, (text, author, likes, rts) in enumerate(self.MOCK_TWEETS):
            # Vary timestamps
            import random
            minutes_ago = random.randint(5, 120)
            timestamp = (base_time - timedelta(minutes=minutes_ago)).isoformat()
            
            mention = TokenMention(
                token_symbol="",
                timestamp=timestamp,
                text=text,
                author=author,
                likes=likes,
                retweets=rts
            )
            mentions.append(mention)
        
        # Add more realistic volume for demo
        for _ in range(15):
            token = random.choice(["PEPE2", "FLOKI"])
            sentiment = random.choice([
                f"${token} to the moon! LFG 🚀",
                f"Bullish on ${token}, huge gem",
                f"${token} is the next 100x",
                f"Just bought more ${token}, feeling good",
                f"${token} breakout incoming, don't miss",
                f"Early alpha: ${token} moon mission",
            ])
            
            mentions.append(TokenMention(
                token_symbol="",
                timestamp=datetime.utcnow().isoformat(),
                text=sentiment,
                author=f"user_{random.randint(1000, 9999)}",
                likes=random.randint(10, 500),
                retweets=random.randint(5, 100)
            ))
        
        print(f"[MockScraper] Generated {len(mentions)} mock mentions")
        
        return mentions


# Import to avoid circular dependency
from datetime import timedelta
