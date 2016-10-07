import Data.List
import Data.List.Split
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

median :: [Double] -> Double
median xs =
    if evenLength
    then medianEven xs
    else medianOdd xs
    where
        evenLength = n `mod` 2 == 0
        n = length xs

        medianEven :: [Double] -> Double
        medianEven xs = mean middle where
            middle = take 2 rightHalf
            rightHalf = drop half sorted
            half = n `div` 2 - 1
            sorted = sort xs
            n = length xs

        medianOdd :: [Double] -> Double
        medianOdd xs = head rightHalf where
            rightHalf = drop half sorted
            half = n `div` 2
            sorted = sort xs
            n = length xs

medianOfMedians :: [Double] -> Double
medianOfMedians xs =
    if length xs < 6 then median xs
    else medianOfMedians ys
        where
            ys = map median xss
            xss = splitEvery 5 xs

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

testMedianOfMedians :: Test
testMedianOfMedians = TestCase (assertEqualFrac 45 (medianOfMedians xs))

testMedianOfMediansLargeInput :: Test
testMedianOfMediansLargeInput = TestCase (assertEqualFrac 54 (medianOfMedians largeXs))

medianTests :: Test
medianTests = TestList [TestLabel "median of list with even length" testMedianEven,
                        TestLabel "median of list with odd length" testMedianOdd,
                        TestLabel "median of medians" testMedianOfMedians,
                        TestLabel "median of medians large input" testMedianOfMediansLargeInput]

main :: IO Counts
main = do _ <- runTestTT meanTests
          runTestTT medianTests
