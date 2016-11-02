import Data.List
import Data.List.Split
import Data.Map (Map)
import qualified Data.Map as Map
import Test.HUnit

mean :: [Double] -> Double
mean xs = sum xs / length' xs

geometricMean :: [Double] -> Double
geometricMean xs = prod ** power where
    prod = product xs
    power = 1 / n
    n = length' xs

harmonicMean :: [Double] -> Double
harmonicMean xs = n * (sum' ** (-1)) where
    n = length' xs
    sum' = sum $ map (\x -> 1 / x) xs

selectFive :: [Double] -> Int -> Double
selectFive xs k = head right where
    right = drop k sorted
    sorted = sort xs

select :: [Double] -> Int -> Double
select xs k
    | n <= threshold = selectFive xs k
    | k < lessN = select less k
    | k == lessN = pivot
    | otherwise = select greater (k - lessN - 1)
    where
        lessN = length less
        less = [x | x <- xs, x < pivot]
        greater = [x | x <- xs, x > pivot]
        pivot = medianOfMedians ys
        ys = map median xss
        xss = splitEvery threshold xs
        n = length xs
        threshold = 5

median :: [Double] -> Double
median xs =
    if evenLength
    then medianEven xs
    else selectFive xs half
    where
        evenLength = n `mod` 2 == 0
        n = length xs
        half = n `div` 2

        medianEven :: [Double] -> Double
        medianEven xs = mean middle where
            middle = take 2 rightHalf
            rightHalf = drop (half - 1) sorted
            sorted = sort xs

medianOfMedians :: [Double] -> Double
medianOfMedians xs = select xs half where
    n = length xs
    half = n `div` 2

mode :: [Double] -> Double
mode xs = helper xs (head xs) (Map.empty) where
    helper :: [Double] -> Double -> Map Double Int -> Double
    helper [] mostFrequentX _ = mostFrequentX
    helper (x:xs) mostFrequentX xToCount = helper xs mostFrequentX' xToCount' where
        mostFrequentX' =
            if Map.lookup x xToCount' > mostFrequentCount
            then x
            else mostFrequentX
        mostFrequentCount = Map.lookup mostFrequentX xToCount'
        xToCount' = Map.insert x count' xToCount
        count' =
            case (Map.lookup x xToCount) of
                Just count -> count + 1
                Nothing -> 0

-- helpers

length' :: [a] -> Double
length' xs = fromIntegral $ length xs

assertEqualFrac :: (Fractional a, Eq a, Ord a, Show a) => a -> a -> Assertion
assertEqualFrac expect value = do _ <- putStr text
                                  assert eq
    where
        text = if eq
               then ""
               else "\n" ++ (show expect) ++ "!=" ++ (show value) ++ "\n"
        eq = (abs (expect - value)) < epsilon
        epsilon = 0.0001

-- tests

xs = [45, 36, 50, 75, 4]
largeXs = [88, 73, 0, 96, 37, 76, 22, 87, 94, 68, 64, 69, 62, 83, 17, 49, 91, 21, 24, 75, 45, 82, 38, 34, 56, 23, 60, 28, 85, 36, 54, 98, 13, 58, 50, 99, 25, 65, 79, 32, 84, 61, 59, 70, 48, 81, 12, 16, 15, 71, 78, 14, 40, 97, 63, 44, 5, 80, 2, 47, 57, 33, 42, 20, 43]

testMean :: Test
testMean = TestCase (assertEqualFrac 42 (mean xs))

testGeometricMean :: Test
testGeometricMean = TestCase (assertEqualFrac 30 (geometricMean xs))

testHarmonicMean :: Test
testHarmonicMean = TestCase (assertEqualFrac 15 (harmonicMean xs))

meanTests :: Test
meanTests = TestList [TestLabel "arithmetic mean" testMean,
                      TestLabel "geometric mean" testGeometricMean,
                      TestLabel "harmonic mean" testHarmonicMean]

testMedianOdd :: Test
testMedianOdd = TestCase (assertEqualFrac 45 (median xs))

testMedianEven :: Test
testMedianEven = TestCase (assertEqualFrac 43 (median $ tail xs))

testMedianOfMedians1 :: Test
testMedianOfMedians1 = TestCase (assertEqualFrac 45 (medianOfMedians xs))

testMedianOfMedians2 :: Test
testMedianOfMedians2 = TestCase (assertEqualFrac 4 (medianOfMedians [1..6]))

testMedianOfMediansLargeInput :: Test
testMedianOfMediansLargeInput = TestCase (assertEqualFrac 56 (medianOfMedians largeXs))

medianTests :: Test
medianTests = TestList [TestLabel "median of list with even length" testMedianEven,
                        TestLabel "median of list with odd length" testMedianOdd,
                        TestLabel "median of medians 1" testMedianOfMedians1,
                        TestLabel "median of medians 2" testMedianOfMedians2,
                        TestLabel "median of medians large input" testMedianOfMediansLargeInput]

modeTest :: Test
modeTest = TestCase (assertEqualFrac 2 (mode [2, 9, 2, 3, 4, 1, 7]))

main :: IO Counts
main = do _ <- runTestTT meanTests
          runTestTT medianTests
          runTestTT modeTest
