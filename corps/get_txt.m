%% -------------------------------------------------------------------
% Descrption : Web file crawler
% Author : Wang Kang
% Mail : goto.champion@gmail.com
% Blog : kang.blog.com
%% -------------------------------------------------------------------
website = 'https://www.gutenberg.org/browse/scores/top'; % the website you want crawling
filetypes = {'txt'}; % file type of downloads during crawling
downloadPath = <path to save downloaded .txt files>; % where to download
if ~isdir(downloadPath)
    mkdir(downloadPath);
end

% start crawling
crawling(website, filetypes, downloadPath)
