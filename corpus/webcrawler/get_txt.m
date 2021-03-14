%% -------------------------------------------------------------------
% Descrption : Web file crawler
% Author : Wang Kang
% Mail : goto.champion@gmail.com
% Blog : kang.blog.com
%% -------------------------------------------------------------------
website = 'https://www.gutenberg.org/browse/scores/top'; % the website you wanna crawling
filetypes = {'txt'}; % the file your wanna download during crawling
downloadPath = 'C:\Users\wilje\OneDrive\Saint Louis University\Courses\Spring 2021\Principles of Software Development\_WordFinder\wordfinder\corpus\gut_dat'; % where to download
if ~isdir(downloadPath)
    mkdir(downloadPath);
end

% start crawling
crawling(website, filetypes, downloadPath)
